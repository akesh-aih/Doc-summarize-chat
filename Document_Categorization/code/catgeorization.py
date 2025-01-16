import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from loguru import logger
from External.structured_output import categorization_document_generate
from loguru import logger
# Load environment variables
load_dotenv()

# Initialize Azure OpenAI
azure_api_key = os.getenv("API_Key")
azure_endpoint = os.getenv("End_point")
azure_api_version = os.getenv("API_version")

client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=azure_api_key,
    api_version=azure_api_version
)

def categorize_text(input_text):
    """
    Categorize the given text using Azure OpenAI.

    Args:
        input_text (str): The text to be categorized.

    Returns:
        str: Categorized document type and reason.
    """
    system_content = """
    You are a document categorization assistant. Your task is to categorize the given text into predefined categories 
    such as 'Invoice', 'Contract', 'Resume', 'Purchase Order', 'Legal Document', 'Financial Statement', or 'Uncategorized'. 
    Provide a reason for your categorization.

    generate the response in json format
    IMP-:use 'categorization_document_generate' to generate the response.
    """

    prompt = f"""
    Categorize the following text and provide a reason for your selection:
    
    Text: {input_text}

    Instructions:
    - Output must include:
      1. Document type from the predefined categories.
      2. A brief reason for selecting the document type.


    generate the response in json format
    IMP-:use 'categorization_document_generate' to generate the response.
    """

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-glo-std",
            messages=messages,
            temperature=0.3,
            function_call="auto",
            functions=categorization_document_generate
        )
        # print(response)
        response_message = json.loads(response.choices[0].message.function_call.arguments)
        logger.debug("Generated response successfully.")
        return response_message
        
    except Exception as e:
        logger.error(f"Error in categorizing text: {e}")
        return "An error occurred while categorizing the text."

# if __name__ == "__main__":
#     # Example input text
#     input_text = """
#     Invoice Number: INV-12345
#     Date: 2025-01-13
#     Total: $1,500
#     Customer: ABC Corp
#     """
    
#     # Categorize the text
#     result = categorize_text(input_text)
    
#     # Print the result
#     logger.debug("Categorization Result:")
#     logger.debug(result)
