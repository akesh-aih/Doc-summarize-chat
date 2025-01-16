import streamlit as st
import os
import json
from Document_Categorization.code.RLHF import RLHF_operator  # Import the RLHF_operator function

# Streamlit Application
def main():
    st.title("AI Document Context Fetcher with Feedback")
    st.sidebar.header("Settings")

    # UUID Path Upload
    st.sidebar.subheader("UUID Path Upload")
    uuid_file = st.sidebar.file_uploader("Upload UUID File (JSON format)", type=["json"], key="uuid_upload")

    if uuid_file:
        uuid_path = os.path.join("temp_uuid", uuid_file.name)
        os.makedirs(os.path.dirname(uuid_path), exist_ok=True)
        with open(uuid_path, "wb") as f:
            f.write(uuid_file.read())
        st.sidebar.success("UUID file uploaded successfully!")
    else:
        st.sidebar.error("Please upload the UUID file to proceed.")

    # Document Path Input
    st.subheader("Document File Path")
    document_path = st.text_input("Enter the file path of the document to process", placeholder="e.g., C:/path/to/document.pdf")

    # Feedback Input
    feedback = st.text_area("Provide Feedback", placeholder="Enter your feedback here...")

    # Process Button
    if st.button("Process Document"):
        if not uuid_file:
            st.error("Please upload the UUID file.")
        elif not document_path.strip():
            st.error("Please provide the document file path.")
        elif not feedback.strip():
            st.error("Feedback is mandatory. Please provide feedback.")
        else:
            with st.spinner("Processing..."):
                try:
                    # Call RLHF_operator
                    result = RLHF_operator(uuid_path, document_path, is_rlhf=True, feedback=feedback)
                    st.success("Processing completed successfully!")
                    st.json(result)
                except Exception as e:
                    st.error(f"Error during processing: {str(e)}")

if __name__ == "__main__":
    main()
