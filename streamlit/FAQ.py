import streamlit as st


def faq_page():
    st.title("Frequently Asked Questions")
    st.write("Here are some common questions and answers:")

    faqs = [
        {
            "question": "What is AI Document Chat?",
            "answer": "AI Document Chat allows you to interact with your documents using AI to get insights.",
        },
        {
            "question": "What types of documents are supported?",
            "answer": "The system supports CSV, PDF, and Excel files.",
        },
        {
            "question": "How secure is my data?",
            "answer": "Your data is stored securely and is not shared with any third parties.",
        },
        {
            "question": "How do I upload documents?",
            "answer": "You can upload your documents via the 'Upload Documents' section once logged in.",
        },
        {
            "question": "How do I create a collection?",
            "answer": "After logging in, use the 'Manage Collections' feature to organize your documents.",
        },
        {
            "question": "How does this application differ from ChatGPT?",
            "answer": (
                "Unlike ChatGPT, where you need to re-upload your files every time you log in and wait for responses, "
                "our application allows you to store your documents in collections permanently. Once uploaded, your documents are always available, "
                "and the AI agent remembers your data, so you don't have to repeat the process every time you log in. This means quicker access "
                "to insights and a more seamless experience."
            ),
        },
    ]

    for faq in faqs:
        with st.expander(f"❓ {faq['question']}"):
            st.write(faq["answer"])
