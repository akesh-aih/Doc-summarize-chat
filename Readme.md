# README

## Overview
This project provides a comprehensive solution for document summarization, categorization, and chatbot interaction. It processes various document formats, summarizes their content, and allows interaction with the user based on extracted summaries or embeddings.

### Features
- **Document Categorization:** Automatically categorizes uploaded documents into predefined categories (e.g., Invoice, Contract, Resume).
- **Summarization:** Extracts and summarizes document content using chunk-based processing for better accuracy.
- **Chatbot Interaction:** Facilitates user interaction with summarized data or embeddings.
- **Embedding and Vector Stores:** Supports embedding generation and retrieval using vector stores.
- **Modular Design:** Organized with reusable components for document loaders, vector stores, and utility functions.

## Prerequisites

1. Python 3.9 or higher.
2. Required libraries (specified in `requirements.txt`).
3. Azure OpenAI API key and endpoint.
4. Redis or other caching mechanisms (optional).

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
Create a `.env` file in the project root with the following variables:
```
API_Key=<your_azure_openai_api_key>
End_point=<your_azure_openai_endpoint>
API_version=<azure_api_version>
```

### Directory Structure
```
project_root/
|-- Chatsupport/
|   |-- code/
|       |-- main.py        # Entry point for chatbot application
|       |-- chat.py        # Chatbot interaction logic
|
|-- Document_Categorization/
|   |-- code/
|       |-- main.py        # Document categorization main script
|
|-- Doc_summarize/
|   |-- code/
|       |-- summarize.py   # Document summarization script
|       |-- chat.py        # Chatbot interaction logic
|       |-- source/
|           |-- loaders/   # File loaders for various document formats
|           |   |-- file_loaders.py
|           |   |-- utils.py
|           |-- vector_store/ # Embedding and vector store utilities
|           |   |-- embedding.py
|           |   |-- utils.py
|
|-- Documentation/         # Documentation for loaders and vector stores
```

## Usage

### Document Summarization
1. Run the summarization script:
    ```bash
    python Doc_summarize/code/summarize.py --uuid <user_id> --document_paths <file_path1> <file_path2>
    ```
    Example:
    ```bash
    python Doc_summarize/code/summarize.py --uuid user123 --document_paths "docs/doc1.pdf" "docs/doc2.pdf"
    ```
2. Summaries will be saved in a user-specific directory under `assets/user-<uuid>/summaries/`.

### Document Categorization
1. Run the document categorization script:
    ```bash
    python Document_Categorization/code/main.py --file_paths <file_path1> <file_path2>
    ```
2. Categorization results will be printed or saved based on configuration.

### Chatbot Interaction
1. Run the chatbot script:
    ```bash
    python Chatsupport/code/main.py --uuid <user_id> --query "<your_query>"
    ```
2. Provide queries to interact with summarized data or document embeddings.

### Streamlit Interface
1. Launch the Streamlit interface:
    ```bash
    streamlit run Chatsupport/code/main.py
    ```
2. Use the graphical interface to upload documents, provide feedback, and interact with the chatbot.

## Key Components

### 1. Document Loaders
- Extracts content from various formats such as PDFs, DOCX, images, and spreadsheets.
- Located in `Doc_summarize/code/source/loaders/`.

### 2. Summarization
- Chunk-based processing ensures high accuracy for large documents.
- Integrated with Azure OpenAI for generating summaries.

### 3. Chatbot
- Provides conversational interfaces using summaries and embeddings.
- Prompts are customized to focus on user queries and document context.

### 4. Embedding and Vector Stores
- Generates and stores embeddings for text and documents.
- Utilizes utilities in `Doc_summarize/code/source/vector_store/`.

## Development

### Testing
Run the test suite using:
```bash
pytest
```

### Extending Functionality
- Add new document loaders in `source/loaders/`.
- Integrate additional vector stores in `source/vector_store/`.
- Customize chatbot behavior in `Chatsupport/code/chat.py`.

## Future Enhancements
- Support for additional file formats.
- Enhanced summarization algorithms with domain-specific fine-tuning.
- Integration with advanced vector stores like Milvus and FAISS.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Support
For support or queries, contact:
- ajinkya@ai-horizon.io
- rushikesh@ai-horizon.io
- akesh@ai-horizon.io