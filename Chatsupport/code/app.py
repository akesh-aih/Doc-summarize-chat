import streamlit as st
import random
import os
from dotenv import load_dotenv
from Chatsupport.code.main import generate_chatbot_response
from Chatsupport.code.main import process_and_store_files

root = os.getcwd()

ALLOWED_FILE_TYPES = [
    "pdf", "txt", "docx", "html", "htm", "rtf", "jpg", "png", "jpeg", "tiff", "csv", "xls", "xlsx", "xlsb"
]

MAX_USER_FILES = 3
MAX_STATIC_FILES = 10

STATIC_DATASET_PATH = os.path.join(root, "assets", "static", "dataset")
os.makedirs(os.path.dirname(STATIC_DATASET_PATH), exist_ok=True)

def main():
    st.title("AI Chat Support")

    if "user_id" not in st.session_state:
        st.session_state.user_id = f"{random.randint(1000, 9999)}{''.join(random.choices(list('abcdefghijklmnopqrstuvwxyz'), k=4))}"

    st.sidebar.header("Input Parameters")

    uuid = st.sidebar.text_input("Enter username", st.session_state.user_id)

    # If the user updates the username, update session state
    if uuid != st.session_state.user_id:
        st.session_state.user_id = uuid

    # Static content file upload (up to 10 files)
    static_files = st.sidebar.file_uploader(
        "Upload static content documents (max 10 files)",
        type=ALLOWED_FILE_TYPES,
        accept_multiple_files=True,
        key="static_upload"
    )

    if static_files and len(static_files) > MAX_STATIC_FILES:
        st.sidebar.error(f"You can upload a maximum of {MAX_STATIC_FILES} static files.")
        static_files = static_files[:MAX_STATIC_FILES]

    if st.sidebar.button("Process Static Content"):
        if not static_files:
            st.sidebar.error("Please upload at least one static content document.")
        else:
            st.toast("Processing static content...")
            static_paths = []
            for uploaded_file in static_files:
                file_path = os.path.join(os.path.dirname(STATIC_DATASET_PATH), uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())
                static_paths.append(file_path)
            process_and_store_files(static_paths, STATIC_DATASET_PATH, overwrite=True)
            st.success("Static content processed successfully.")

    # User-specific file upload (up to 3 files)
    user_files = st.sidebar.file_uploader(
        "Upload your documents (max 3 files)",
        type=ALLOWED_FILE_TYPES,
        accept_multiple_files=True,
        key="user_upload"
    )

    if user_files and len(user_files) > MAX_USER_FILES:
        st.sidebar.error(f"You can upload a maximum of {MAX_USER_FILES} files.")
        user_files = user_files[:MAX_USER_FILES]

    if st.sidebar.button("Process User Documents"):
        if not uuid:
            st.sidebar.error("Please enter a UUID.")
        elif not user_files:
            st.sidebar.error("Please upload at least one user document.")
        else:
            load_dotenv()
            user_dir = os.path.join(root, "assets", f"user-{uuid}")
            user_dataset_path = os.path.join(user_dir, "dataset")
            os.makedirs(user_dir, exist_ok=True)

            st.toast("Processing user documents...")

            user_paths = []
            for uploaded_file in user_files:
                file_path = os.path.join(user_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())
                user_paths.append(file_path)

            # Process the uploaded files
            process_and_store_files(user_paths, user_dataset_path, overwrite=True)

            st.success("User documents processed successfully. You can now ask questions.")

            # Initialize chat history in session state
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

    if "chat_history" in st.session_state:
        query = st.text_input("Type your question here:", placeholder="Ask me anything...")

        if st.button("Send Query"):
            if not query.strip():
                st.error("Please enter a valid query.")
            else:
                try:
                    response_text = generate_chatbot_response(
                        user_id=uuid,
                        input_path="",
                        query=query,
                        file_paths=static_paths + user_paths if 'static_paths' in locals() and 'user_paths' in locals() else [],
                    )
                except Exception as e:
                    response_text = f"Error generating response: {str(e)}"

                # Append query and response to chat history
                st.session_state.chat_history.append({"query": query, "response": response_text})

                # Display query and response
                st.chat_message("user").write(query)
                st.chat_message("assistant").write(response_text)

    # Display chat history
    if "chat_history" in st.session_state and st.session_state.chat_history:
        st.subheader("Chat History")
        for chat in st.session_state.chat_history:
            st.chat_message("user").write(chat["query"])
            st.chat_message("assistant").write(chat["response"])

if __name__ == "__main__":
    main()
