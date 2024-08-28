import streamlit as st
from db_utils import get_user_collections
from document_service import DocumentService
from streamlit_chat import message


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "document_service" not in st.session_state:
        st.session_state.document_service = DocumentService(
            api_key="your_api_key", embedding_model="your_model"
        )
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""


def display_chat_messages():
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            message(msg["content"], is_user=True, key=f"msg_{i}")
        else:
            message(msg["content"], key=f"msg_{i}")


def process_input():
    if st.session_state.user_input:
        user_question = st.session_state.user_input
        st.session_state.messages.append({"role": "user", "content": user_question})

        with st.spinner("Thinking..."):
            try:
                response = st.session_state.document_service.ask_question(user_question)
                if response:
                    ai_response = response.response
                    st.session_state.messages.append(
                        {"role": "assistant", "content": ai_response}
                    )

                    # Display sources in a collapsible section
                    if response.source_nodes:
                        with st.expander("View Sources"):
                            for node_with_score in response.source_nodes:
                                node = node_with_score.node
                                st.markdown(f"**Text Snippet:** *{node.text[:200]}...*")
                                st.markdown("---")
                else:
                    st.error(
                        "Unable to find an answer. Please try rephrasing your question."
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")

        # Clear the input after processing
        st.session_state.user_input = ""


def chat_page():
    init_session_state()

    st.sidebar.title("💬 Document Chat")

    if "user" in st.session_state and st.session_state.user:
        user_id = st.session_state.user[0]
        collections = get_user_collections(user_id)

        if collections:
            selected_collection = st.sidebar.selectbox(
                "Choose a collection", collections
            )
            if selected_collection:
                st.session_state.document_service.setup_index(
                    selected_collection, is_existing=True
                )
                st.sidebar.success(f"Chatting with: {selected_collection}")
        else:
            st.sidebar.info(
                "You don't have any collections yet. Go to the Collections page to create one!"
            )
    else:
        st.sidebar.warning("Please log in to chat with your documents.")
        return

    st.title("Chat with Your Documents")
    display_chat_messages()

    st.text_input(
        "Ask a question about your documents:",
        key="user_input",
        on_change=process_input,
    )
