import streamlit as st
import os
from db_utils import create_db
from document_service import DocumentService
from llama_index.embeddings.openai import OpenAIEmbedding

# Create the database
create_db()

# Set up the Streamlit app
st.set_page_config(
    page_title="AI Chat with Your Documents", page_icon="📄", layout="wide"
)

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None
if "document_service" not in st.session_state:
    st.session_state.document_service = DocumentService(
        api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
        embedding_model=OpenAIEmbedding(),
    )
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"  # Default page


if st.session_state.page == "🏠 Home":
    # Import and show the Home page logic
    from pages.Home import home_page

    home_page()

elif st.session_state.page == "📁 Collections" and st.session_state.user:
    # Import and show the Collections page
    from pages.Collections import collections_page

    collections_page()

elif st.session_state.page == "🤖 Chat" and st.session_state.user:
    # Import and show the Chat page
    from pages.Chat import chat_page

    chat_page()

elif st.session_state.page == "❓ FAQ":
    from pages.FAQ import faq_page

    faq_page()

elif st.session_state.page == "📧 Contact Us":
    from pages.ContactUs import contact_us_page

    contact_us_page()
