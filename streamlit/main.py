import os
import streamlit as st
from streamlit_option_menu import option_menu
from llama_index.embeddings.openai import OpenAIEmbedding
from Home import home_page
from Chat import chat_page
from Collections import collections_page
from ContactUs import contact_us_page
from FAQ import faq_page
from db_services import DBService
from document_service import DocumentService  # Import DBService if needed

# Set up the Streamlit app
st.set_page_config(
    page_title="AI Chat with Your Documents", page_icon="📄", layout="wide"
)

# Custom CSS for styling sidebar and other elements
st.markdown(
    """
    <style>
    /* Custom styling for the sidebar */
    .css-1l02m7d { /* Adjust this class if necessary */
        width: 320px; /* Increase the width of the sidebar */
    }
    .css-1v3fvcr { /* Adjust this class if necessary */
        font-size: 22px; /* Increase font size of text in the sidebar */
    }
    .css-1v3fvcr i { /* Increase size of icons in the sidebar */
        font-size: 24px;
    }
    .css-1v3fvcr .st-bd { /* Increase padding for sidebar items */
        padding: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar navigation
with st.sidebar:
    selected_page = option_menu(
        menu_title=None,
        options=["🏠 Home", "📁 Collections", "🤖 Chat", "❓ FAQ", "📧 Contact Us"],
        icons=["house", "folder", "chat-dots", "question-circle", "envelope"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#282c34"},
            "icon": {"font-size": "24px", "color": "#61dafb"},  # Increase icon size
            "nav-link": {
                "font-size": "20px",  # Increase text size
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#21a1f1",
            },
            "nav-link-selected": {"background-color": "#61dafb"},
        },
    )

# Initialize the document service
if "document_service" not in st.session_state:
    st.session_state.document_service = DocumentService(
        api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
        embedding_model=OpenAIEmbedding(),
    )

# Map selected page to functions
if selected_page == "🏠 Home":
    home_page()
elif selected_page == "📁 Collections":
    collections_page()
elif selected_page == "🤖 Chat":
    chat_page()
elif selected_page == "❓ FAQ":
    faq_page()
elif selected_page == "📧 Contact Us":
    contact_us_page()
