import streamlit as st
import pandas as pd
from db_utils import get_user_collections
from services.document_service import DocumentService
import textwrap
import time


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = {}
    if "document_service" not in st.session_state:
        user_id = st.session_state.get("user", {}).get("id", "default_user")
        st.session_state.document_service = DocumentService(
            api_key="your_api_key", embedding_model="your_model"
        )
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "current_collection" not in st.session_state:
        st.session_state.current_collection = None
    if "thinking" not in st.session_state:
        st.session_state.thinking = False


def display_chat_messages(collection_name):
    if collection_name not in st.session_state.messages:
        st.session_state.messages[collection_name] = []

    for msg in st.session_state.messages[collection_name]:
        role = "human" if msg["role"] == "user" else "ai"
        content = msg["content"]

        if isinstance(content, pd.DataFrame):
            st.markdown(f"<div class='chat-message {role}'>", unsafe_allow_html=True)
            st.dataframe(content)
            st.markdown("</div>", unsafe_allow_html=True)
        elif "table_html" in msg:
            st.markdown(f"<div class='chat-message {role}'>", unsafe_allow_html=True)
            st.markdown(msg["table_html"], unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            icon = "🤖" if role == "ai" else "👤"
            st.markdown(
                f"""
                <div class='chat-message {role}'>
                    <div class='icon'>{icon}</div>
                    <div class='message-content'>{content}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )


def format_table_response(df):
    return df.to_html(index=False, classes=["table", "table-striped", "table-hover"])


def process_input(user_id: int, collection_name: str):
    if st.session_state.user_input:
        user_question = st.session_state.user_input
        if collection_name not in st.session_state.messages:
            st.session_state.messages[collection_name] = []
        st.session_state.messages[collection_name].append(
            {"role": "user", "content": user_question}
        )

        st.session_state.thinking = True

        try:
            # Check if the collection is initialized
            if not st.session_state.document_service.is_collection_initialized(
                collection_name
            ):
                st.error(
                    f"Collection '{collection_name}' is not initialized. Please set up the index first."
                )
                st.session_state.thinking = False
                return

            document_type = st.session_state.document_service.get_document_type(
                collection_name
            )
            response = st.session_state.document_service.ask_question(
                user_id, collection_name, user_question
            )
            if response:
                if isinstance(response, pd.DataFrame):
                    table_html = format_table_response(response)
                    st.session_state.messages[collection_name].append(
                        {
                            "role": "assistant",
                            "content": "Here's the data you requested:",
                            "table_html": table_html,
                        }
                    )
                elif document_type in ["csv", "excel"]:
                    formatted_response = f"As an AI data analyst, here's my analysis based on the {document_type.upper()} file:\n\n{response}"
                    st.session_state.messages[collection_name].append(
                        {"role": "assistant", "content": formatted_response}
                    )
                elif document_type == "pdf":
                    formatted_response = textwrap.fill(response, width=80)
                    formatted_response += (
                        "\n\nFor more details, please refer to the PDF document."
                    )
                    st.session_state.messages[collection_name].append(
                        {"role": "assistant", "content": formatted_response}
                    )
                else:
                    st.session_state.messages[collection_name].append(
                        {"role": "assistant", "content": str(response)}
                    )
            else:
                st.error(
                    "Unable to find an answer. Please try rephrasing your question."
                )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

        st.session_state.thinking = False
        st.session_state.user_input = ""


def chat_page():
    init_session_state()

    st.sidebar.title("💬 Document Chat")

    if "user" in st.session_state and st.session_state.user:
        user_id = st.session_state.user["id"]
        collections = get_user_collections(user_id)

        if collections:
            selected_collection = st.sidebar.selectbox(
                "Choose a collection", collections
            )
            if selected_collection:
                collection_name = selected_collection[0]

                # Provjera je li kolekcija inicijalizirana
                if not st.session_state.document_service.is_collection_initialized(
                    collection_name
                ):
                    st.warning(
                        f"Collection '{collection_name}' is not initialized. Initializing now..."
                    )
                    try:
                        st.session_state.document_service.setup_index(
                            collection_name, is_existing=True
                        )
                        st.success(
                            f"Successfully initialized collection: {collection_name}"
                        )
                    except Exception as e:
                        st.error(
                            f"Error initializing collection {collection_name}: {str(e)}"
                        )
                        return

                if collection_name != st.session_state.current_collection:
                    st.session_state.current_collection = collection_name

                document_type = st.session_state.document_service.get_document_type(
                    collection_name
                )
                st.sidebar.info(
                    f"Chatting with: {collection_name} ({document_type.upper()})"
                )

                st.title(f"Chat with {collection_name}")

                chat_container = st.container()
                with chat_container:
                    display_chat_messages(collection_name)

                if st.session_state.thinking:
                    st.markdown(
                        """
                        <div class='chat-message ai thinking-message'>
                            <div class='icon'>🤖</div>
                            <div class='message-content'>
                                <div class="thinking-bubble">
                                    Razmišljam<div class="dot"></div>
                                    <div class="dot"></div>
                                    <div class="dot"></div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                user_input = st.text_input(
                    "Ask a question about your documents:",
                    key="user_input",
                    on_change=process_input,
                    args=(user_id, collection_name),
                )
        else:
            st.info(
                "You don't have any collections yet. Go to the Collections page to create one!"
            )
    else:
        st.warning("Please log in to chat with your documents.")
        return

    st.markdown(
        """
    <style>
        /* Bubble animation CSS */
    .thinking-bubble {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100px;
        height: 30px;
        background-color: #3a3a3a;
        border-radius: 15px;
        position: relative;
    }
    .thinking-bubble .dot {
        width: 8px;
        height: 8px;
        background-color: #e0e0e0;
        border-radius: 50%;
        margin: 0 3px;
        animation: bounce 1.3s linear infinite;
    }
    .thinking-bubble .dot:nth-child(2) {
        animation-delay: -1.1s;
    }
    .thinking-bubble .dot:nth-child(3) {
        animation-delay: -0.9s;
    }
    @keyframes bounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-8px); }
    }
    body {
        color: #e0e0e0;
        background-color: #1e1e1e;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1300px;
    }
    .stTextInput > div > div > input {
        background-color: #2b2b2b;
        border: 1px solid #444;
        border-radius: 0.375rem;
        color: #e0e0e0;
        font-size: 18px;
        padding: 0.75rem 1rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #0969da;
        box-shadow: 0 0 0 3px rgba(9, 105, 218, 0.3);
    }
    .chat-message {
        display: flex;
        margin-bottom: 1.5rem;
        align-items: flex-start;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .chat-message .icon {
        font-size: 32px;
        margin-right: 1rem;
        min-width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background-color: #2b2b2b;
    }
    .chat-message .message-content {
        background-color: #2b2b2b;
        border-radius: 0.5rem;
        padding: 1rem;
        font-size: 18px;
        line-height: 1.5;
        max-width: calc(100% - 70px);
    }
    .chat-message.human {
        flex-direction: row-reverse;
    }
    .chat-message.human .icon {
        margin-right: 0;
        margin-left: 1rem;
        background-color: #0969da;
        color: white;
    }
    .chat-message.human .message-content {
        background-color: #0969da;
        color: white;
    }
    .chat-message.ai .message-content {
        background-color: #2b2b2b;
        color: #e0e0e0;
    }
    .thinking-message .message-content {
        padding: 0.5rem;
    }
    .thinking-bubble {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 30px;
        background-color: #3a3a3a;
        border-radius: 15px;
    }
    .thinking-bubble .dot {
        width: 8px;
        height: 8px;
        background-color: #e0e0e0;
        border-radius: 50%;
        margin: 0 3px;
        animation: bounce 1.3s linear infinite;
    }
    .thinking-bubble .dot:nth-child(2) {
        animation-delay: -1.1s;
    }
    .thinking-bubble .dot:nth-child(3) {
        animation-delay: -0.9s;
    }
    @keyframes bounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-8px); }
    }
    /* Styling for dataframes */
    .dataframe {
        border-collapse: collapse;
        margin: 1rem 0;
        font-size: 0.9em;
        font-family: sans-serif;
        min-width: 400px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        background-color: #2b2b2b;
        color: #e0e0e0;
    }
    .dataframe thead tr {
        background-color: #0969da;
        color: #ffffff;
        text-align: left;
    }
    .dataframe th,
    .dataframe td {
        padding: 12px 15px;
        border-bottom: 1px solid #444;
    }
    .dataframe tbody tr:nth-of-type(even) {
        background-color: #333;
    }
    .dataframe tbody tr:last-of-type {
        border-bottom: 2px solid #0969da;
    }
    /* Responsive design */
    @media (max-width: 768px) {
        .chat-message {
            flex-direction: column;
        }
        .chat-message .icon {
            margin-bottom: 0.5rem;
        }
        .chat-message .message-content {
            max-width: 100%;
        }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
