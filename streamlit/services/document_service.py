import os
from typing import List, Dict, Optional, Tuple, Union
import pandas as pd
import streamlit as st
import logging
from llama_index.core import VectorStoreIndex, StorageContext, Document, ServiceContext
from llama_parse import LlamaParse
from llama_index.vector_stores.qdrant import QdrantVectorStore
from services.db_services import DBService
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.query_engine import PandasQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
import nest_asyncio

# Apply async loop patch
nest_asyncio.apply()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserSession:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.chat_history: Dict[str, List[Dict[str, str]]] = {}

    def add_message(self, collection_name: str, role: str, content: str):
        if collection_name not in self.chat_history:
            self.chat_history[collection_name] = []
        self.chat_history[collection_name].append({"role": role, "content": content})

    def get_chat_history(self, collection_name: str) -> List[Dict[str, str]]:
        return self.chat_history.get(collection_name, [])


class DocumentService:
    def __init__(
        self,
        api_key: str,
        embedding_model: str,
        language: str = "en",
        result_type: str = "markdown",
    ):
        logger.info("Initializing DocumentService...")
        self.api_key = api_key
        self.embedding_model = embedding_model
        self.language = language
        self.result_type = result_type
        self.index: Optional[VectorStoreIndex] = None
        self.db = DBService()
        self.collection_initialized = False
        self.document_type: Dict[str, str] = {}
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
        self.agents: Dict[str, ReActAgent] = {}
        self.user_sessions: Dict[str, UserSession] = {}
        self.memory_buffers: Dict[str, ChatMemoryBuffer] = {}
        self.dataframes: Dict[str, pd.DataFrame] = {}
        logger.info("DocumentService initialized successfully.")

    def get_user_session(self, user_id: str) -> UserSession:
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = UserSession(user_id)
        return self.user_sessions[user_id]

    def setup_index(
        self,
        collection_name: str,
        documents_path: Optional[str] = None,
        is_existing: bool = False,
    ) -> None:
        logger.info(f"Setting up index for collection: {collection_name}")
        try:
            vector_store = QdrantVectorStore(
                client=self.db.client, collection_name=collection_name
            )
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            if is_existing:
                self.index = VectorStoreIndex.from_vector_store(vector_store)
                logger.info(f"Using existing collection: {collection_name}")
            else:
                if documents_path is None:
                    raise ValueError(
                        "documents_path must be provided for new collections"
                    )

                documents, doc_type = self.load_documents(documents_path)
                if not documents:
                    raise ValueError(
                        "Parsed documents are empty. Please check the file."
                    )

                self.document_type[collection_name] = doc_type

                service_context = ServiceContext.from_defaults(llm=self.llm)
                self.index = VectorStoreIndex.from_documents(
                    documents=documents,
                    storage_context=storage_context,
                    service_context=service_context,
                    show_progress=True,
                )
                logger.info(f"New collection {collection_name} created and indexed.")

            self.collection_initialized = True
            self.setup_agent(collection_name)
            logger.info(f"Index setup completed for collection: {collection_name}")

        except Exception as e:
            logger.error(f"Error setting up index: {e}")
            st.error(f"Error setting up index: {str(e)}")
            self.index = None
            self.collection_initialized = False

    def load_documents(self, documents_path: str) -> Tuple[List[Document], str]:
        _, file_extension = os.path.splitext(documents_path)
        supported_extensions = [".pdf", ".docx", ".txt", ".csv", ".xlsx"]

        if file_extension.lower() not in supported_extensions:
            raise ValueError(
                f"Unsupported file format: {file_extension}. Supported formats are: {', '.join(supported_extensions)}"
            )

        logger.info(f"Loading documents from: {documents_path}")
        if file_extension.lower() in [".csv", ".xlsx"]:
            return self.load_data_from_dataframe(documents_path, file_extension)
        else:
            return self.load_data_from_parser(documents_path), "pdf"

    def load_data_from_dataframe(
        self, documents_path: str, file_extension: str
    ) -> Tuple[List[Document], str]:
        logger.info(f"Loading data from a {file_extension} file.")
        df = (
            pd.read_csv(documents_path)
            if file_extension.lower() == ".csv"
            else pd.read_excel(documents_path)
        )
        text_content = df.to_string()
        logger.info("Data loaded from dataframe successfully.")
        logger.info(
            f"Data preview: {text_content[:1000]}..."
        )  # Print first 1000 chars for sanity check
        self.dataframes[documents_path] = df
        return [
            Document(text=text_content, extra_info={"dataframe": df})
        ], file_extension[1:]

    def load_data_from_parser(self, documents_path: str) -> List[Document]:
        logger.info(f"Parsing document using LlamaParse: {documents_path}")
        parser = LlamaParse(
            api_key=self.api_key, result_type=self.result_type, language=self.language
        )
        documents = parser.load_data(documents_path)
        logger.info("Documents parsed successfully using LlamaParse.")
        return documents

    def setup_agent(self, collection_name: str) -> None:
        logger.info(f"Setting up ReAct agent for collection: {collection_name}")
        if self.index is None:
            raise ValueError("Index is not initialized. Call setup_index first.")

        retriever = VectorIndexRetriever(index=self.index, similarity_top_k=5)
        query_engine = RetrieverQueryEngine.from_args(
            retriever, service_context=ServiceContext.from_defaults(llm=self.llm)
        )

        tools = [
            QueryEngineTool(
                query_engine=query_engine,
                metadata=ToolMetadata(
                    name="document_qa",
                    description=f"Provides information from the {collection_name} collection. The document type is {self.document_type.get(collection_name, 'unknown')}. For PDF documents, provide page numbers for citations.",
                ),
            ),
        ]

        if self.document_type.get(collection_name) in ["csv", "xlsx"]:
            df = next(iter(self.dataframes.values()), None)
            if df is not None:
                pandas_query_engine = PandasQueryEngine(df, verbose=True)
                tools.append(
                    QueryEngineTool(
                        query_engine=pandas_query_engine,
                        metadata=ToolMetadata(
                            name="data_analysis",
                            description=f"Performs data analysis on the {collection_name} {self.document_type.get(collection_name)} file. Provide answers in table format when appropriate.",
                        ),
                    )
                )

        memory = self.memory_buffers.get(
            collection_name, ChatMemoryBuffer.from_defaults(token_limit=2000)
        )
        self.memory_buffers[collection_name] = memory

        self.agents[collection_name] = ReActAgent.from_tools(
            tools,
            llm=self.llm,
            memory=memory,
            verbose=True,
        )
        logger.info(f"ReAct agent setup complete for collection: {collection_name}")

    def ask_question(
        self, user_id: str, collection_name: str, question: str
    ) -> Optional[Union[str, pd.DataFrame]]:
        logger.info(
            f"Asking question for user {user_id} in collection {collection_name}: {question}"
        )
        if collection_name not in self.agents:
            raise ValueError(
                f"Agent for collection {collection_name} is not initialized. Call setup_index first."
            )

        try:
            user_session = self.get_user_session(user_id)
            user_session.add_message(collection_name, "user", question)

            agent = self.agents[collection_name]
            chat_history = user_session.get_chat_history(collection_name)
            context = f"You are an AI assistant analyzing a {self.document_type.get(collection_name, 'unknown')} document. "
            context += f"Previous conversation: {chat_history}\n\nUser: {question}"

            response_obj = agent.chat(context)
            response = str(response_obj.response)

            if self.document_type.get(collection_name) in ["csv", "xlsx"]:
                if self.should_format_as_table(question):
                    df = self.dataframes.get(next(iter(self.dataframes.keys())))
                    if df is not None:
                        table_response = self.format_response_as_table(response, df)
                        user_session.add_message(
                            collection_name, "assistant", table_response
                        )
                        return table_response
                else:
                    formatted_response = (
                        f"As an AI data analyst, here's my analysis:\n\n{response}"
                    )
                    user_session.add_message(
                        collection_name, "assistant", formatted_response
                    )
                    return formatted_response
            elif self.document_type.get(collection_name) == "pdf":
                formatted_response = self.format_pdf_response(response)
                user_session.add_message(
                    collection_name, "assistant", formatted_response
                )
                return formatted_response
            else:
                user_session.add_message(collection_name, "assistant", str(response))
                return str(response)
        except Exception as e:
            logger.error(f"Error while asking the question: {e}")
            st.error(f"Error while asking the question: {e}")
            return None

    def should_format_as_table(self, question: str) -> bool:
        keywords = [
            "first",
            "top",
            "bottom",
            "last",
            "row",
            "column",
            "show",
            "display",
            "list",
        ]
        return any(keyword in question.lower() for keyword in keywords)

    def format_response_as_table(self, response: str, df: pd.DataFrame) -> str:
        try:
            # Attempt to extract a subset of the dataframe based on the response
            if "first" in response.lower() or "top" in response.lower():
                num_rows = int("".join(filter(str.isdigit, response)))
                result_df = df.head(num_rows)
            elif "last" in response.lower() or "bottom" in response.lower():
                num_rows = int("".join(filter(str.isdigit, response)))
                result_df = df.tail(num_rows)
            else:
                # If no specific subset is mentioned, return the full dataframe
                result_df = df

            # Convert the dataframe to a markdown table
            markdown_table = result_df.to_markdown(index=False)
            return f"Here's the requested data in table format:\n\n{markdown_table}"
        except Exception as e:
            logger.error(f"Error formatting response as table: {e}")
            return str(response)  # Return the original response if formatting fails

    def format_pdf_response(self, response: str) -> str:
        # Implement logic to extract page numbers and format citations
        # This is a placeholder implementation and should be customized based on your PDF structure
        formatted_response = "Based on the PDF content:\n\n"
        formatted_response += response
        formatted_response += (
            "\n\nFor more details, please refer to the specific pages mentioned above."
        )
        return formatted_response

    def get_agent(self, collection_name: str) -> Optional[ReActAgent]:
        return self.agents.get(collection_name)

    def get_document_type(self, collection_name: str) -> str:
        """
        Vraća tip dokumenta za danu kolekciju.
        """
        return self.document_type.get(collection_name, "unknown")

    @staticmethod
    def load_prompt(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
