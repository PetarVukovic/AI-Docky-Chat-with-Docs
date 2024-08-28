import streamlit as st
from db_utils import get_user_collections
from document_service import (
    DocumentService,
)  # Pretpostavljam da se koristi DocumentService iz document_service.py


def display_response(response):
    st.markdown("### 💡 **Answer:**")
    st.markdown(
        f"<div style='font-size: 20px; font-weight: bold; color: green;'>{response.response}</div>",
        unsafe_allow_html=True,
    )

    if response.source_nodes:
        st.markdown("### 📚 **Sources:**")
        for node_with_score in response.source_nodes:
            node = node_with_score.node
            st.markdown("---")
            st.markdown(f"**Source ID:** `{node.id_}`")
            st.markdown(f"**Text Snippet:** *{node.text[:200]}...*")


def chat_page():
    if "user" in st.session_state and st.session_state.user:
        st.title("💬 Chat with Your Documents")

        user_id = st.session_state.user[0]
        collections = get_user_collections(user_id)

        if collections:
            selected_collection = st.selectbox("Choose a collection", collections)

            if selected_collection:
                # Ensure DocumentService is initialized
                if "document_service" not in st.session_state:
                    st.session_state.document_service = DocumentService(
                        api_key="your_api_key", embedding_model="your_model"
                    )

                st.session_state.document_service.setup_index(
                    selected_collection, is_existing=True
                )

                st.subheader(f"Chat with: {selected_collection}")
                user_question = st.text_input("Ask a question about your documents:")
                if st.button("Ask"):
                    if user_question:
                        with st.spinner("Searching for an answer..."):
                            try:
                                # Call ask_question directly without asyncio.run
                                response = (
                                    st.session_state.document_service.ask_question(
                                        user_question
                                    )
                                )
                                if response:
                                    display_response(response)
                                else:
                                    st.error(
                                        "Unable to find an answer. Please try rephrasing your question."
                                    )
                            except Exception as e:
                                st.error(f"An error occurred: {e}")
                    else:
                        st.warning("Please enter a question.")

            st.subheader("Document Preview")
            st.info("Document preview functionality to be implemented.")
        else:
            st.info(
                "You don't have any collections yet. Go to the Collections page to create one!"
            )
    else:
        st.info("Please log in to chat with your documents.")
