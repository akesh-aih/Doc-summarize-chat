import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from Document_Categorization.code.category import *
from Document_Categorization.code.index_fetch import *
from rich import print


import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from loguru import logger
# from structured_output import invoice_data_extractor,purchase_order_data_extractor,contract_data_extractor,financial_statement_data_extractor
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

def generate_summry(feedback_data):
    """
    Generate a summary after reaching the threshold.
    """
    system_content = f"""
    You are a professional financial statement parser designed to extract important details from financial statements. 
    Your task is to analyze the data and generate a summary that highlights the overall intent and purpose of the financial statement.

    Your summary should:
    - Focus on key insights, such as financial obligations, stability, risks, or opportunities.
    - Provide an overview of short-term and long-term financial priorities.
    - Highlight the relevance of the financial data to decision-making or planning.

    Example:
    "The financial statement's primary intent is to emphasize the need for effective cash flow management to meet upcoming 
    obligations. It highlights the importance of maintaining financial stability while focusing on addressing short-term liabilities. 
    The summary underscores the significance of balancing immediate payments and long-term goals."

    Note: Your response should provide a concise and clear intent for the final data, avoiding specific details unless critical for understanding.
    """

    prompt = f"""
Analyze the following financial statement data and generate a summary that highlights its intent and purpose:

feedback_data: {feedback_data}

Instructions:
1. Focus on the overarching intent of the financial statement, such as emphasizing financial obligations, stability, or areas of improvement.
2. Avoid mentioning specific dates unless they are critical to understanding the intent.
3. Highlight the relevance of the data to financial decision-making, planning, or addressing specific risks or opportunities.
4. Ensure the summary is concise, clear, and focused on the broader financial priorities.

Example Summary:
"The financial statement emphasizes the need for efficient cash flow management to address immediate obligations while 
ensuring financial stability. It highlights the importance of balancing short-term liabilities with long-term financial goals, 
providing insights for better decision-making."

Now, generate a summary that conveys the intent and purpose of the provided financial statement data.
"""


    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-glo-std",
            messages=messages,
            temperature=0.3

        )
        # print(response)
        # print(response)
        # input("Press Enter to continue...")
        logger.debug("Generated response successfully.")
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error in categorizing text: {e}")
        return "An error occurred while categorizing the text."

# import json

# def generate_summary(data):
#     """
#     Generate a summary of the JSON list data.
#     Replace this function with your actual summary logic.
#     """
#     # Example summary logic
#     summary = {
#         "total_elements": len(data),
#         "first_element": data[0] if len(data) > 0 else None,
#         "last_element": data[-1] if len(data) > 0 else None
#     }
#     return summary

def count_elements_in_json(file_path, threshold=10):
    """
    Open a JSON file with a list structure, count its elements,
    and generate a summary if the count exceeds a threshold.
    """
    try:
        # Open and load the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if the internal structure is a list
        if isinstance(data, list):
            count = len(data)
            # print(f"The JSON file contains {count} elements.")
        else:
            print("The internal structure of the JSON file is not a list.")
            count = 0
        
        # Check if the count exceeds the threshold
        if count >= threshold:
            summary = generate_summry(data)
            # input("Press Enter to continue...")
            return summary


    except Exception as e:
        print(f"Error occurred: {e}")
        return ''

# Example usage



def save_to_json(data, directory="output"):
    """Save data 
    to a JSON file with a UUID-based filename."""
    # Ensure the output directory exists
    import os
    os.makedirs(directory, exist_ok=True)
    
    # Generate a unique filename
    file_name = f"{uuid.uuid4()}.json"
    file_path = os.path.join(directory, file_name)
    
    # Save the data to the JSON file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
    print(f"Saved output to {file_path}")


def indentify_context_fetcher(file_paths: list, feedback_path: str, threshold: int = 10):
    """
    Process files to extract document data and handle feedback in JSON.
    Generates summaries if feedback count exceeds the threshold.
    """
    Output_result = []

    # Step 1: Check feedback count and generate summary if necessary
    summary = count_elements_in_json(feedback_path, threshold=threshold)
    if summary:
        print("Summary generated:", summary)

    # Step 2: Categorize the documents
    output = categorize_document(file_paths=file_paths)

    def process_text_data(text_data):
        """Fetch context and details for each document."""
        file_path = text_data['file']
        extracted_text = text_data['text']
        document_type = text_data['document_type']

        # Generate a unique UUID for this file/document
        file_uuid = str(uuid.uuid4())

        # Fetch data based on the document type
        fetched_data = index_fetch(document_type, extracted_text,is_rlhf=False,feedback_intent=summary)

        # Prepare the final output with UUID
        final_output = {
            'uuid': file_uuid,
            'file': file_path,
            'document_type': document_type,
            'final_data': fetched_data
        }
        return final_output

    # Step 3: Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(process_text_data, output)

    # Collect the results into Output_result
    Output_result = list(results)
    print(Output_result)
    # Step 4: Save the output as JSON
    save_to_json(Output_result)

    return Output_result


# Example file paths
# file_paths = [
#     r"C:\Users\Rushikesh\Desktop\Hridayam\document_category\test_1.png",
#     r"C:\Users\Rushikesh\Desktop\Hridayam\document_category\test_2.png"
# ]

# # Call the function
# indentify_context_fetcher(file_paths, r"C:\Users\Rushikesh\Desktop\Hridayam\feedback.json")

# file_path = r"C:\Users\Rushikesh\Desktop\Hridayam\feedback.json"
# count_elements_in_json(file_path)


# file_path = r"C:\Users\Rushikesh\Desktop\Hridayam\feedback.json"
# threshold = 1
# result = count_elements_in_json(file_path, threshold=threshold)
# if result:
#     print("Summary:", result)
