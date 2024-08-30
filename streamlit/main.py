import os
import streamlit as st
from streamlit_option_menu import option_menu
from llama_index.embeddings.openai import OpenAIEmbedding
from Home import home_page
from Chat import chat_page
from Collections import collections_page
from ContactUs import contact_us_page
from FAQ import faq_page
from services.db_services import DBService
from services.document_service import DocumentService
from Pricing import pricing_page
from UserSettings import user_settings_page
from Login import login_page

# Set up the Streamlit app
st.set_page_config(
    page_title="AI Chat with Your Documents", page_icon="📄", layout="wide"
)

# Initialize session state for user
if "user" not in st.session_state:
    st.session_state.user = None

# Custom CSS for styling sidebar and other elements
st.markdown(
    """
    <style>
    /* Custom styling for the sidebar */
    .css-1l02m7d {
        width: 320px;
    }
    .css-1v3fvcr {
        font-size: 22px;
    }
    .css-1v3fvcr i {
        font-size: 24px;
    }
    .css-1v3fvcr .st-bd {
        padding: 15px;
    }
    /* User info styling */
    .user-info {
        padding: 10px;
        background-color: #3a3a3a;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .user-info img {
        width: 50px;
        height: 50px;
        border-radius: 25px;
        margin-right: 10px;
    }
    .user-info span {
        vertical-align: middle;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar navigation
with st.sidebar:
    if st.session_state.user:
        st.markdown(
            f"""
            <div class="user-info">
                <img src="https://via.placeholder.com/50" alt="User Avatar">
                <span>{st.session_state.user['username']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    selected_page = option_menu(
        menu_title=None,
        options=[
            "🏠 Home",
            "📁 Collections",
            "🤖 Chat",
            "❓ FAQ",
            "📧 Contact Us",
            "💳 Pricing",
            "⚙️ Settings",
            "🚪 Logout" if st.session_state.user else "🔑 Login/Register",
        ],
        icons=[
            "house",
            "folder",
            "chat-dots",
            "question-circle",
            "envelope",
            "credit-card",
            "gear",
            "box-arrow-right" if st.session_state.user else "box-arrow-in-right",
        ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#282c34"},
            "icon": {"font-size": "24px", "color": "#61dafb"},
            "nav-link": {
                "font-size": "20px",
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
elif selected_page == "💳 Pricing":
    pricing_page()
elif selected_page == "⚙️ Settings":
    user_settings_page()
elif selected_page == "🚪 Logout":
    st.session_state.user = None
    st.rerun()
elif selected_page == "🔑 Login/Register":
    login_page()
