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
    ]

    for faq in faqs:
        with st.expander(f"❓ {faq['question']}"):
            st.write(faq["answer"])


if __name__ == "__main__":
    faq_page()
