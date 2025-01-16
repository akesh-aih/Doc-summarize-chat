import streamlit as st
import os
import random
import uuid
from main import indentify_context_fetcher, count_elements_in_json, save_to_json  # Import necessary functions

# Define constants
ALLOWED_FILE_TYPES = [
    "pdf", "txt", "docx", "html", "htm", "rtf", "jpg", "png", "jpeg", "tiff", "csv", "xls", "xlsx", "xlsb"
]
MAX_FILES = 10  # Maximum number of files that can be uploaded
FEEDBACK_FILE_PATH = r"C:\Users\Rushikesh\Desktop\Hridayam\feedback.json"  # Static feedback file path

# Streamlit Application
def main():
    st.title("AI Document Context Fetcher")
    st.sidebar.header("Settings")

    # Initialize session state
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"{random.randint(1000, 9999)}{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=4))}"

    uuid = st.sidebar.text_input("Enter UUID (optional)", st.session_state.user_id)

    # Document Upload
    uploaded_files = st.file_uploader("Upload Documents", type=ALLOWED_FILE_TYPES, accept_multiple_files=True, key="doc_upload")
    file_paths = []
    if uploaded_files:
        temp_dir = "temp_files"
        os.makedirs(temp_dir, exist_ok=True)
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            file_paths.append(file_path)
        st.success("Documents uploaded successfully!")

    # Process documents
    if st.button("Process Documents"):
        if not uploaded_files:
            st.error("Please upload at least one document.")
        else:
            with st.spinner("Processing documents..."):
                try:
                    # Call the function from main.py with is_rlhf set to False
                    results = indentify_context_fetcher(file_paths, FEEDBACK_FILE_PATH, threshold=10)
                    st.success("Processing completed!")
                
                    # Display results in the Streamlit UI
                    st.json(results)
                except Exception as e:
                    st.error(f"Error during processing: {str(e)}")

    # Optional: Display feedback summary
    with st.spinner("Generating feedback summary..."):
        try:
            summary = count_elements_in_json(FEEDBACK_FILE_PATH, threshold=10)
            if summary:
                st.write("Feedback Summary:")
                st.success(summary)
        except Exception as e:
            st.error(f"Error generating summary: {str(e)}")

if __name__ == "__main__":
    main()
