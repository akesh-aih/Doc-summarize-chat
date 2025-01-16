import streamlit as st
import os
import random
from extract_text import FileTextExtractor
from image_support import extract_image_text
from concurrent.futures import ThreadPoolExecutor

# Initialize the text extractor
extract_text = FileTextExtractor()

# Define allowed file types
ALLOWED_FILE_TYPES = [
    "pdf", "txt", "docx", "html", "htm", "rtf", "jpg", "png", "jpeg", "tiff", "csv", "xls", "xlsx", "xlsb"
]

# Function to extract text from a single file
def fetch_invoice_text(file_path):
    if file_path.endswith(('.pdf', '.docx', '.txt', '.html', '.htm', '.rtf', '.tiff', '.csv', '.xls', '.xlsx', '.xlsb')):
        return extract_text.extract_text_from_file(file_path)
    elif file_path.endswith(('.jpg', '.jpeg', '.png')):
        return extract_image_text(file_path)
    else:
        return f"Unsupported file format: {file_path}"

# Wrapper function to process a single file for use with ThreadPoolExecutor
def process_single_file(file_path):
    text = fetch_invoice_text(file_path)
    if text:
        return {'file': file_path, 'text': text}
    else:
        return {'file': file_path, 'text': 'Error: Unsupported file format or empty content.'}

# Process multiple files in parallel
def process_multiple_files(file_paths):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_single_file, file_paths))
    return results

# Save uploaded files to a directory
def save_uploaded_files(uploaded_files, destination_dir):
    file_paths = []
    os.makedirs(destination_dir, exist_ok=True)
    for uploaded_file in uploaded_files:
        file_path = os.path.join(destination_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        file_paths.append(file_path)
    return file_paths

# Main Streamlit app
def main():
    st.title("Invoice Text Extractor")

    # Initialize session state for user ID
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"{random.randint(1000, 9999)}{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=4))}"

    # Sidebar input
    st.sidebar.header("File Uploads")
    user_id = st.sidebar.text_input("User ID", st.session_state.user_id)

    # File uploads
    uploaded_files = st.sidebar.file_uploader(
        "Upload files for text extraction and viewing",
        type=ALLOWED_FILE_TYPES,
        accept_multiple_files=True
    )

    if st.sidebar.button("Process Files"):
        if uploaded_files:
            user_dir = os.path.join("uploads", user_id)
            file_paths = save_uploaded_files(uploaded_files, user_dir)

            # Process files in parallel
            with st.spinner("Processing files..."):
                extracted_texts = process_multiple_files(file_paths)

            # Display extracted text and file viewers
            st.success("Files processed successfully!")
            for entry in extracted_texts:
                file_name = os.path.basename(entry['file'])

                # Create two columns: Left for image/file, right for text
                col1, col2 = st.columns([3, 3])  # Equal proportions for image and text

                with col1:
                    st.write(f"**File:** {file_name}")
                    if file_name.endswith(('.jpg', '.jpeg', '.png', '.tiff')):
                        # Display image
                        st.image(entry['file'], caption=file_name, use_column_width=True)
                        if st.button(f"Enlarge {file_name}"):
                            with st.expander("Enlarged View", expanded=True):
                                # Enlarged image view
                                col_image, col_text = st.columns([3, 2])  # Larger focus on image
                                with col_image:
                                    st.image(entry['file'], use_column_width=True, caption=file_name)
                                with col_text:
                                    # Display extracted text with white background and font
                                    st.markdown(
                                        f"<div style='background-color: black; color: white; padding: 10px; height: 500px; overflow-y: auto;'>{entry['text']}</div>",
                                        unsafe_allow_html=True,
                                    )
                    elif file_name.endswith('.pdf'):
                        with open(entry['file'], "rb") as pdf_file:
                            pdf_data = pdf_file.read()
                        st.download_button("Download PDF", pdf_data, file_name=file_name, mime="application/pdf")
                        st.write("PDF preview is currently unavailable.")
                    else:
                        st.write("Preview not available for this file type.")

                with col2:
                    # Display extracted text
                    st.text_area("Extracted Text", entry["text"], height=400, key=file_name)

                st.markdown("---")  # Separator for better UI
        else:
            st.sidebar.error("No files uploaded!")

if __name__ == "__main__":
    main()
