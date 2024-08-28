import streamlit as st
import asyncio
from db_utils import get_user_collections


def display_response(response):
    # Prikaz odgovora
    st.markdown("### 💡 **Answer:**")
    st.markdown(
        f"<div style='font-size: 20px; font-weight: bold; color: green;'>{response.response}</div>",
        unsafe_allow_html=True,
    )

    # Prikaz izvora ako ih ima
    if response.source_nodes:
        st.markdown("### 📚 **Sources:**")
        for node_with_score in response.source_nodes:
            node = node_with_score.node
            st.markdown("---")  # Razdjelnik između izvora

            # Prikaz ID-a izvora
            st.markdown(f"**Source ID:** `{node.id_}`")

            # Prikaz isječka teksta
            st.markdown(f"**Text Snippet:** *{node.text[:200]}...*")


st.set_page_config(page_title="Chat with Documents", page_icon="💬")

if "user" in st.session_state and st.session_state.user:
    st.title("💬 Chat with Your Documents")

    user_id = st.session_state.user[0]
    collections = get_user_collections(user_id)

    if collections:
        selected_collection = st.selectbox("Choose a collection", collections)

        if selected_collection:
            st.session_state.document_service.setup_index(
                selected_collection, is_existing=True
            )

            st.subheader(f"Chat with: {selected_collection}")
            user_question = st.text_input("Ask a question about your documents:")
            if st.button("Ask"):
                if user_question:
                    with st.spinner("Searching for an answer..."):
                        response = asyncio.run(
                            st.session_state.document_service.ask_question(
                                user_question
                            )
                        )
                        # Prikaz odgovora
                        if response:
                            display_response(response)

                        else:
                            st.error(
                                "Unable to find an answer. Please try rephrasing your question."
                            )
                else:
                    st.warning("Please enter a question.")

            # Display document summary or preview
            st.subheader("Document Preview")
            # Implement the document preview functionality here
            st.info("Document preview functionality to be implemented.")
    else:
        st.info(
            "You don't have any collections yet. Go to the Collections page to create one!"
        )
else:
    st.info("Please log in to chat with your documents.")
