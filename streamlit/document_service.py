import os
import pandas as pd
import streamlit as st
from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_parse import LlamaParse
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from db_services import DBService


class DocumentService:
    def __init__(self, api_key, embedding_model, language="en", result_type="markdown"):
        self.api_key = api_key
        self.embedding_model = embedding_model
        self.language = language
        self.result_type = result_type
        self.index = None
        self.db = DBService()
        self.collection_initialized = False  # Inicijalizacija kolekcije

    def setup_index(
        self,
        collection_name: str,
        documents_path: str = None,
        is_existing: bool = False,
    ) -> None:
        try:
            vector_store = QdrantVectorStore(
                client=self.db.client, collection_name=collection_name
            )
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            if is_existing:
                # Ako kolekcija već postoji, postavi indeks iz vektorske trgovine
                self.index = VectorStoreIndex.from_vector_store(vector_store)
            else:
                if documents_path is None:
                    raise ValueError(
                        "documents_path must be provided for new collections"
                    )

                # Provjera podržanih ekstenzija
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

                # Kreiranje indeksa iz dokumenata
                self.index = VectorStoreIndex.from_documents(
                    documents=documents,
                    storage_context=storage_context,
                    show_progress=True,
                )

            self.collection_initialized = True  # Oznaka da je kolekcija inicijalizirana

        except Exception as e:
            st.error(f"Error setting up index: {str(e)}")
            self.index = None
            self.collection_initialized = (
                False  # U slučaju greške, kolekcija nije inicijalizirana
            )

    def load_documents(self, documents_path, file_extension):
        if file_extension.lower() in [".csv", ".xlsx"]:
            return self.load_data_from_dataframe(documents_path, file_extension)
        else:
            return self.load_data_from_parser(documents_path)

    def load_data_from_dataframe(self, documents_path, file_extension):
        if file_extension.lower() == ".csv":
            df = pd.read_csv(documents_path)
        else:  # .xlsx
            df = pd.read_excel(documents_path)
        text_content = df.to_string()
        return [Document(text=text_content)]

    def load_data_from_parser(self, documents_path):
        parser = LlamaParse(
            api_key=self.api_key,
            result_type=self.result_type,
            language=self.language,
        )
        return parser.load_data(documents_path)

    def ask_question(self, question: str) -> str:
        if not self.collection_initialized:
            raise ValueError("Index is not initialized. Call setup_index first.")

        try:
            query_engine = self.index.as_query_engine()
            response = query_engine.query(question)  # Ukloni 'await'
            return response
        except Exception as e:
            st.error(f"Error while asking the question: {e}")
            return None

    def get_document_summary(self, documents_path: str) -> str:
        # Implementacija funkcije za sažimanje dokumenata
        st.info("DOCS SUMMARY")
        pass
