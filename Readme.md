# README

## Overview

This project provides an advanced document summarization and chatbot application capable of processing various document formats, summarizing content, and interacting with users using reference data.

### Features
- Document summarization for PDFs, DOCX, and other supported formats.
- Chunk-based processing for large documents.
- Asynchronous and retry-enabled document processing.
- Integration with Azure OpenAI for embeddings and text generation.
- Storage and retrieval using vector databases like DeepLake and Weaviate.
- Professional chatbot interactions leveraging document summaries and vector embeddings.

## Prerequisites

1. Python 3.9+
2. Required libraries (see `requirements.txt`)
3. Azure OpenAI API key and endpoint
4. Redis setup for caching (optional but recommended)
5. Additional tools: PyMuPDF, PyPDF4, python-docx

## Setup

### Clone Repository
```bash
git clone <repository_url>
cd <project_directory>
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file and configure the following variables:
```
API_Key=<your_azure_openai_api_key>
End_point=<your_azure_openai_endpoint>
API_version=<azure_api_version>
```

### Directory Structure
```
project_root/
|-- assets/                  # Stores user-specific files, summaries, etc.
|-- source/
|   |-- loaders/             # Document loaders
|   |-- vector_store/        # Embedding and vector store utilities
|   |-- utils.py             # Utility functions
|-- main.py                  # Entry point for the application
|-- summarize.py             # Summarization logic
|-- chat.py                  # Chatbot interaction
```

## Usage

### Document Summarization
1. Run the summarization app:
    ```bash
    python summarize.py --uuid <user_id> --document_paths <file_path1> <file_path2>
    ```
    Example:
    ```bash
    python summarize.py --uuid user123 --document_paths "docs/doc1.pdf" "docs/doc2.pdf"
    ```
2. The summaries will be saved under `assets/user-<uuid>/summaries/`.

### Chatbot Interaction
1. Run the chatbot app:
    ```bash
    python chat.py --uuid <user_id> --query "<your_query>" --chat_with summary|document
    ```
    Example:
    ```bash
    python chat.py --uuid user123 --query "What is the purpose of this document?" --chat_with document
    ```

### Streamlit Interface
Run the Streamlit app for a graphical user interface:
```bash
streamlit run main.py
```

## Key Components

### 1. Document Processing
- **File Loaders:** Extracts text content from PDFs and DOCX files.
- **Chunking:** Splits text into manageable sizes with overlaps for better summarization and embedding.

### 2. Summarization
- **Async Summarization:** Generates summaries for each chunk using Azure OpenAI models.
- **Retry Logic:** Ensures robustness by retrying failed requests.

### 3. Embedding and Vector Stores
- **Azure Embeddings:** Generates embeddings for text and queries.
- **DeepLake Integration:** Stores and retrieves embeddings for document-based queries.

### 4. Chatbot Interaction
- **Prompt Engineering:** Customizes chatbot responses to focus on provided document data.
- **LinearSyncPipeline:** Ensures structured execution of tasks.

## API References

### Summarization Functions
- `async_summarize_document(chunks)`: Summarizes chunks asynchronously.
- `generate_summary(context)`: Generates a single summary for the provided context.

### Chatbot Functions
- `chatbot(query, reference_text, messages, chat_with, summary_dir)`: Handles chatbot interaction based on summaries or vector embeddings.

### Utility Functions
- `retry_async`: Retry logic for asynchronous operations.
- `chunk_text`: Splits text into manageable chunks.

## Development

### Testing
Run the tests with:
```bash
pytest
```


## Future Enhancements
- Support for additional document formats.
- Advanced filtering and ranking for retrieved chunks.
- Integration with more vector stores (e.g., Milvus, FAISS).

## License
[MIT License](LICENSE)

## Support
For issues or questions, 
contact -:
- ajinkya@ai-horizon.io,
- rushikesh@ai-horizon.io,
- akesh@ai-horizon.io.