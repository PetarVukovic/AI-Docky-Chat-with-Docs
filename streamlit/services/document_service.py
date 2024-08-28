import os
import pandas as pd
import streamlit as st
from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_parse import LlamaParse
from llama_index.vector_stores.qdrant import QdrantVectorStore
from services.db_services import DBService
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import ToolMetadata
import nest_asyncio

nest_asyncio.apply()


class DocumentService:
    """
    Service for handling document processing, indexing, and querying with integrated RAGReActAgent.
    """

    def __init__(self, api_key, embedding_model, language="en", result_type="markdown"):
        """
        Initialize the DocumentService.

        :param api_key: API key for LlamaParse and OpenAI
        :param embedding_model: Name of the embedding model to use
        :param language: Language of the documents (default: "en")
        :param result_type: Type of result to return (default: "markdown")
        """
        self.api_key = api_key
        self.embedding_model = embedding_model
        self.language = language
        self.result_type = result_type
        self.index = None
        self.db = DBService()
        self.collection_initialized = False
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
        self.agent = None

    def setup_index(
        self,
        collection_name: str,
        documents_path: str = None,
        is_existing: bool = False,
    ) -> None:
        """
        Set up the vector index for document storage and retrieval.

        :param collection_name: Name of the Qdrant collection
        :param documents_path: Path to the documents (required for new collections)
        :param is_existing: Whether the collection already exists
        """
        try:
            vector_store = QdrantVectorStore(
                client=self.db.client, collection_name=collection_name
            )
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            if is_existing:
                self.index = VectorStoreIndex.from_vector_store(vector_store)
            else:
                if documents_path is None:
                    raise ValueError(
                        "documents_path must be provided for new collections"
                    )

                _, file_extension = os.path.splitext(documents_path)
                supported_extensions = [".pdf", ".docx", ".txt", ".csv", ".xlsx"]

                if file_extension.lower() not in supported_extensions:
                    raise ValueError(
                        f"Unsupported file format: {file_extension}. Supported formats are: {', '.join(supported_extensions)}"
                    )

                documents = self.load_documents(documents_path, file_extension)

                if not documents:
                    raise ValueError(
                        "Parsed documents are empty. Please check the file."
                    )

                self.index = VectorStoreIndex.from_documents(
                    documents=documents,
                    storage_context=storage_context,
                    show_progress=True,
                )

            self.collection_initialized = True
            self.setup_agent(collection_name)

        except Exception as e:
            st.error(f"Error setting up index: {str(e)}")
            self.index = None
            self.collection_initialized = False

    def load_documents(self, documents_path, file_extension):
        """
        # Load documents from the given path based on the file extension.

        :param documents_path: Path to the document file
        :param file_extension: Extension of the document file
        :return: List of Document objects
        """
        if file_extension.lower() in [".csv", ".xlsx"]:
            return self.load_data_from_dataframe(documents_path, file_extension)
        else:
            return self.load_data_from_parser(documents_path)

    def load_data_from_dataframe(self, documents_path, file_extension):
        """
        Load data from CSV or Excel files.

        :param file_extension: Extension of the data file
        :return: List containing a single Document object with the data as text
        """
        if file_extension.lower() == ".csv":
            df = pd.read_csv(documents_path)
        else:  # .xlsx
            df = pd.read_excel(documents_path)
        text_content = df.to_string()
        return [Document(text=text_content)]

    def load_data_from_parser(self, documents_path):
        """
        Load data using LlamaParse for PDF, DOCX, and TXT files.

        :param documents_path: Path to the document file
        :return: List of Document objects parsed by LlamaParse
        """
        parser = LlamaParse(
            api_key=self.api_key,
            result_type=self.result_type,
            language=self.language,
        )
        return parser.load_data(documents_path)

    def setup_agent(self, collection_name: str):
        """
        Set up the ReAct agent with the document index.

        :param collection_name: Name of the Qdrant collection
        """
        if self.index is None:
            raise ValueError("Index is not initialized. Call setup_index first.")

        query_engine = self.index.as_query_engine(similarity_top_k=3)

        query_engine_tool = QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name=collection_name,
                description=f"Provides information from the document collection '{collection_name}'. "
                "Use a detailed plain text question as input to the tool.",
            ),
        )

        self.agent = ReActAgent.from_tools(
            [query_engine_tool], llm=self.llm, verbose=True
        )

    def ask_question(self, question: str):
        """
        Ask a question to the ReAct agent.

        :param question: The question to ask
        :return: The agent's response to the question
        """
        if not self.collection_initialized or self.agent is None:
            raise ValueError("Agent is not initialized. Call setup_index first.")

        try:
            response = self.agent.chat(question)
            return response
        except Exception as e:
            st.error(f"Error while asking the question: {e}")
            return None
