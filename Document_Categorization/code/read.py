import os
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
    """
    Extract text from a file based on its format.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Extracted text or an error message.
    """
    if file_path.endswith(('.pdf', '.docx', '.txt', '.html', '.htm', '.rtf', '.tiff', '.csv', '.xls', '.xlsx', '.xlsb')):
        return extract_text.extract_text_from_file(file_path)
    elif file_path.endswith(('.jpg', '.jpeg', '.png')):
        return extract_image_text(file_path)
    else:
        return f"Unsupported file format: {file_path}"

# Wrapper function to process a single file
def process_single_file(file_path):
    """
    Process a single file to extract text.

    Args:
        file_path (str): Path to the file.

    Returns:
        dict: Dictionary containing file path and extracted text.
    """
    text = fetch_invoice_text(file_path)
    if text:
        return {'file': file_path, 'text': text}
    else:
        return {'file': file_path, 'text': 'Error: Unsupported file format or empty content.'}

# Process multiple files in parallel
def process_multiple_files(file_paths):
    """
    Process multiple files in parallel to extract text.

    Args:
        file_paths (list): List of file paths.

    Returns:
        list: List of dictionaries containing file paths and extracted texts.
    """
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_single_file, file_paths))
    return results




# Example usage
# if __name__ == "__main__":
#     # Replace with your file paths
#     file_paths = [
#         r"C:\Users\Rushikesh\Desktop\Hridayam\document_category\Picture.pdf",
#         r"C:\Users\Rushikesh\Desktop\Hridayam\document_category\Picture.pdf",
#         r"C:\Users\Rushikesh\Desktop\Hridayam\document_category\test_2.png"
#     ]

#     # Process files and fetch extracted text
#     extracted_texts = process_multiple_files(file_paths)

#     # Display the extracted text for each file
#     for entry in extracted_texts:
#         print(f"File: {entry['file']}")
#         print(f"Extracted Text: {entry['text']}")
#         print("-" * 50)
