from External.extract_text import FileTextExtractor
from External.image_support import extract_image_text


# Initialize the text extractor
extract_text = FileTextExtractor()


def fetch_invoice_text(file_path):
    """
    Fetch text from an invoice file. Supports multiple file formats like PDF, DOCX, TXT, and images (JPG, PNG, etc.)

    Args:
        file_path (str): Path to the invoice file.

    Returns:
        str: Extracted text from the file.
    """
    if file_path.endswith(('.pdf', '.docx', '.txt', '.html', '.htm', '.rtf', '.tiff', '.csv', '.xls', '.xlsx', '.xlsb')):
        return extract_text.extract_text_from_file(file_path)
    elif file_path.endswith('.jpg') or file_path.endswith('.png') or file_path.endswith('.jpeg'):
        reviver_text = extract_image_text(file_path)
        return reviver_text
    else:
        print(f"Unsupported file format: {file_path}")
        return None


def process_multiple_files(file_paths):
    """
    Process multiple files and fetch their text content.

    Args:
        file_paths (list): List of file paths to process.

    Returns:
        list: A list of extracted texts from all files.
    """
    all_texts = []
    for file_path in file_paths:
        text = fetch_invoice_text(file_path)
        if text:
            all_texts.append({
                'file': file_path,
                'text': text
            })
        else:
            all_texts.append({
                'file': file_path,
                'text': 'Error: Unsupported file format or empty content.'
            })
    return all_texts


# Example usage
file_paths = [
    r"C:\Users\Rushikesh\Desktop\POCS\crown_ww_poc\sample\test_1.png"
]

extracted_texts = process_multiple_files(file_paths)

# Print or process the extracted texts
for entry in extracted_texts:
    print(f"File: {entry['file']}\nExtracted Text: {entry['text'][:500]}...\n")