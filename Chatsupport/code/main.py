import argparse
import os
import sys
import json
import uuid
from dotenv import load_dotenv
from External.vector import DeepLakeManager, add_custom_nodes, query_custom_embedding
from aih_rag.embeddings.azure_openai import AzureOpenAIEmbedding
from structured_output import chat_response
from openai import AzureOpenAI
from Chatsupport.code.extract_text import FileTextExtractor
from memory import RedisCache
from loguru import logger
# Load environment variables
load_dotenv()

# Initialize Azure OpenAI
azure_api_key = os.getenv("API_Key")
azure_endpoint = os.getenv("End_point")
azure_api_version = os.getenv("API_version")

azure_embedding = AzureOpenAIEmbedding(
    model="text-embedding-3-small",
    azure_endpoint=azure_endpoint,
    api_key=azure_api_key,
    api_version="2024-02-01",
    azure_deployment="text-embedding-3-small"
)

client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=azure_api_key,
    api_version=azure_api_version
)

# JSON file to maintain user dataset mappings
USER_DATASET_FILE = "user_dataset.json"
redis_cache = RedisCache()

def load_user_dataset_mapping():
    """Load the user-to-dataset mapping from the JSON file."""
    if os.path.exists(USER_DATASET_FILE):
        with open(USER_DATASET_FILE, "r") as f:
            return json.load(f)
    return {}


def save_user_dataset_mapping(mapping):
    """Save the user-to-dataset mapping to the JSON file."""
    with open(USER_DATASET_FILE, "w") as f:
        json.dump(mapping, f, indent=4)


def get_user_dataset_path(user_id):
    """
    Get the dataset path for a given user.

    Args:
        user_id (str): Unique user ID.

    Returns:
        str: Path to the user's dataset, or None if not found.
    """
    mapping = load_user_dataset_mapping()
    return mapping.get(user_id)


def update_user_dataset_path(user_id, dataset_path):
    """
    Update the dataset path for a user in the mapping.

    Args:
        user_id (str): Unique user ID.
        dataset_path (str): Path to the user's dataset.
    """
    mapping = load_user_dataset_mapping()
    mapping[user_id] = dataset_path
    save_user_dataset_mapping(mapping)


def create_dataset_path(base_dir, subfolder, user_id=None):
    """
    Create a dataset path for content or user-specific datasets.

    Args:
        base_dir (str): Base directory for datasets.
        subfolder (str): Subfolder name (e.g., "content" or "users").
        user_id (str): Unique user ID (optional for user-specific datasets).

    Returns:
        str: Path to the dataset.
    """
    if user_id:
        user_dir = os.path.join(base_dir, subfolder, user_id)
        os.makedirs(user_dir, exist_ok=True)
        return os.path.join(user_dir, f"dataset_{uuid.uuid4().hex}")
    else:
        content_dir = os.path.join(base_dir, subfolder)
        os.makedirs(content_dir, exist_ok=True)
        return os.path.join(content_dir, "dataset")


def chunk_text(text, chunk_size=1000, overlap=100):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def initialize_store(dataset_path, overwrite=False):
    """
    Initialize DeepLakeManager.

    Args:
        dataset_path (str): Path to the Deep Lake dataset.
        overwrite (bool): Whether to overwrite the dataset if it already exists.

    Returns:
        DeepLakeManager: Initialized DeepLakeManager instance.
    """
    try:
        return DeepLakeManager(dataset_path=dataset_path, overwrite=overwrite)
    except Exception as e:
        logger.debug(f"Error initializing dataset at {dataset_path}: {e}")
        raise


def process_and_store_files(file_paths, dataset_path, overwrite=False):
    """
    Process multiple files and store their chunks and embeddings in a DeepLake dataset.

    Args:
        file_paths (list): List of file paths to process.
        dataset_path (str): Path to the DeepLake dataset.
        overwrite (bool): Whether to overwrite the dataset if it already exists.
    """

    extract_text = FileTextExtractor()
    chunks = []
    embeddings = []

    for file_path in file_paths:
        try:
            logger.debug(f"Processing file: {file_path}")
            text = extract_text.extract_text_from_file(file_path)
            file_chunks = chunk_text(text=text, chunk_size=2000, overlap=100)
            chunks.extend(file_chunks)

            # Generate embeddings for each chunk
            for chunk in file_chunks:
                chunk_embedding = azure_embedding.get_text_embedding(text=chunk)
                embeddings.append(chunk_embedding)
        except Exception as e:
            logger.debug(f"Error processing file {file_path}: {e}")

    if chunks and embeddings:
        # Initialize the dataset
        manager = initialize_store(dataset_path, overwrite=overwrite)
        add_custom_nodes(manager, chunks, embeddings)
    else:
        logger.debug(f"No valid content found in the provided files. Skipping dataset creation.")


def fetch_relevant_chunks(query, dataset_paths):
    """
    Fetch relevant chunks from multiple DeepLake datasets based on a query.

    Args:
        query (str): Query string.
        dataset_paths (list): List of DeepLake dataset paths.

    Returns:
        list: Relevant chunks retrieved from datasets.
    """
    relevant_chunks = []
    query_embedding = azure_embedding.get_text_embedding(text=query)

    for dataset_path in dataset_paths:
        if not os.path.exists(dataset_path):
            logger.debug(f"Dataset path {dataset_path} does not exist. Skipping.")
            continue
        try:
            manager = initialize_store(dataset_path)
            chunks = query_custom_embedding(manager, query_embedding=query_embedding)
            logger.debug(f"Found {len(chunks)} relevant chunks in dataset: {dataset_path}")
            if chunks:
                relevant_chunks.extend(chunks)
        except Exception as e:
            logger.debug(f"Error querying dataset at {dataset_path}: {e}")

    return relevant_chunks

def generate_chatbot_response(user_id, input_path, query, file_paths=[], base_dir="chatsupport\temp"):
    cached_response = redis_cache.check_cached_response(query)
    if cached_response:
        logger.debug("Cache hit! Returning cached response.")
        print(cached_response)
        return cached_response

    os.makedirs(base_dir, exist_ok=True)
    content_dataset_path = os.path.join(base_dir, "content", "dataset")
    os.makedirs(os.path.dirname(content_dataset_path), exist_ok=True)

    user_dataset_path = get_user_dataset_path(user_id)
    if not user_dataset_path:
        user_dataset_path = create_dataset_path(base_dir, subfolder="users", user_id=user_id)

    try:
        if file_paths:
            logger.debug("Processing static content files...")
            process_and_store_files(file_paths, content_dataset_path, overwrite=False)

        if input_path:
            logger.debug(f"Processing user file for user ID {user_id}...")
            process_and_store_files([input_path], user_dataset_path, overwrite=True)
            update_user_dataset_path(user_id, user_dataset_path)



        dataset_paths = [content_dataset_path, user_dataset_path]
        relevant_chunks = fetch_relevant_chunks(query, dataset_paths)
        reference_text = "\n".join(relevant_chunks) if relevant_chunks else "No relevant data found."

        system_content = """
        You are a professional chatbot that is helpful and friendly.
        IMP_:Output must be markdown format.
        """

        prompt = f"""
        Generate a chatbot-like response to the following query using the reference text in a descriptive, pointwise format:

        query: {query}
        reference text: {reference_text}

        Instructions:
        - Use the reference text to answer the query directly.
        - Provide the response in a descriptive, pointwise format.
        - Ensure the tone is professional yet conversational, suitable for a chatbot.
        - Clearly highlight key points or steps.
        - Conclude with a friendly and professional closing statement.
        """

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-glo-std",
            messages=messages,
            temperature=0.3
        )

        response_content = response.choices[0].message.content
        redis_cache.cache_response(query, response_content)
        logger.debug("Generated response successfully.")
        print(response_content)
        return response_content

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "An error occurred while generating the response."



# # Example usage
# generate_chatbot_response(
#     user_id="user123",
#     input_path=r"C:\Users\Rushikesh\Desktop\Hridayam\summaizer\LongRAG Enhancing Retrieval-Augmented Generation with Long-context LLMs (1).pdf",
#     query="what is rag mechanism in automobile and BFSI",
#     # uuid_path="output.json",
#     file_paths=[r"C:\Users\Rushikesh\Desktop\Hridayam\summaizer\LongRAG Enhancing Retrieval-Augmented Generation with Long-context LLMs (1).pdf"]
# )
