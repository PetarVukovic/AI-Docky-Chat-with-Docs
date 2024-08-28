import streamlit as st
import os
from db_utils import register_user, login_user


def home_page():
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        .css-18e3th9 { 
            background-color: #000000; 
            color: #ffffff;
        }
        .css-18e3th9 .stText {
            color: #ffffff;
        }
        .css-18e3th9 .stButton {
            background-color: #007bff;
            color: #ffffff;
            border-radius: 5px;
            border: none;
            padding: 10px;
            margin-top: 10px;
        }
        .css-18e3th9 .stButton:hover {
            background-color: #0056b3;
        }
        .main-content {
            color: #ffffff;
            font-family: 'Arial', sans-serif;
        }
        .main-content h1 {
            color: #ffffff;
            font-size: 2em;
        }
        .main-content p {
            font-size: 1.2em;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Main content for the home page
    st.markdown(
        '<div class="main-content"><h1>Welcome to AI Chat with Your Documents 🤖</h1>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="main-content">
        <p>This is your one-stop application to interact with your documents using advanced AI technology. Navigate through the features to manage your documents, chat with the AI, and more.</p>
        <h2>Features</h2>
        <ul>
            <li>📂 <strong>Upload Documents:</strong> Add CSV, PDF, and Excel files.</li>
            <li>📁 <strong>Manage Collections:</strong> Organize your documents for easy access.</li>
            <li>🤖 <strong>Chat with AI:</strong> Get insights and answers from your documents.</li>
        </ul>
        <h2>Advanced AI Technologies</h2>
        <p>The AI can process various types of documents, helping you extract information and understand data better. It works with:</p>
        <ul>
            <li>📊 <strong>CSV Files:</strong> Summarize and analyze tabular data.</li>
            <li>📄 <strong>PDF Files:</strong> Process complex PDFs with tables and graphs.</li>
            <li>📈 <strong>Excel Files:</strong> Extract and analyze data from spreadsheets.</li>
        </ul>
        <p>For example, you can ask questions like, <i>"What is the average revenue in the last quarter?"</i> and receive accurate answers based on your data.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar for login and registration
    with st.sidebar:
        st.markdown("<h1>👤 User Authentication</h1>", unsafe_allow_html=True)

        if st.session_state.user:
            st.write(f"Logged in as: {st.session_state.user[1]}")
            if st.button("Logout"):
                st.session_state.user = None
                st.rerun()
        else:
            auth_option = st.radio("Choose option", ["Login", "Register"])
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if auth_option == "Login":
                st.markdown("<h2>🔑 Login</h2>", unsafe_allow_html=True)
                if st.button("Login"):
                    user = login_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.success(f"Welcome {username}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            else:
                st.markdown("<h2>✍️ Register</h2>", unsafe_allow_html=True)
                if st.button("Register"):
                    if username and password:
                        register_user(username, password)
                        st.success("Registration successful! Please log in.")
                    else:
                        st.error("Please enter both username and password")
