import streamlit as st
import tempfile
import os
from db_utils import add_collection_to_user, get_user_collections


st.set_page_config(page_title="Collections", page_icon="📚")
if "user" in st.session_state and st.session_state.user:
    st.title("📚 Your Collections")
    user_id = st.session_state.user[0]
    collections = get_user_collections(user_id)
    st.subheader("Create a New Collection")
    new_collection_name = st.text_input("Collection name")
    uploaded_files = st.file_uploader(
        "Upload documents (max 3)",
        accept_multiple_files=True,
        type=["pdf", "docx", "txt", "csv", "xlsx"],
    )
    if st.button("Create Collection"):
        if new_collection_name and uploaded_files:
            if len(uploaded_files) <= 3:
                add_collection_to_user(user_id, new_collection_name)
                for uploaded_file in uploaded_files:
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=os.path.splitext(uploaded_file.name)[1],
                    ) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    try:
                        st.session_state.document_service.setup_index(
                            new_collection_name,
                            tmp_file_path,
                            is_existing=False,
                        )
                    finally:
                        os.remove(tmp_file_path)
                st.success(
                    f"Collection '{new_collection_name}' created with {len(uploaded_files)} document(s)!"
                )
                st.rerun()
            else:
                st.error("You can upload a maximum of 3 files.")
        else:
            st.error(
                "Please provide a collection name and upload at least one document."
            )
    st.subheader("Your Existing Collections")
    if collections:
        for collection in collections:
            st.write(f"- {collection}")
    else:
        st.info("You don't have any collections yet. Create one above!")
else:
    st.info("Please log in to view and manage your collections.")
