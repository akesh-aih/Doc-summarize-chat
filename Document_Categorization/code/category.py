from read import process_multiple_files
from Document_Categorization.code.catgeorization import categorize_text
# from rich import print



from concurrent.futures import ThreadPoolExecutor

def categorize_document(file_paths):
    output = []
    extracted_texts = process_multiple_files(file_paths)
    
    def process_entry(entry):
        """Process each entry to categorize the document."""
        text = entry['text']
        file_path = entry['file']
        result = categorize_text(text[:100])
        return {
            "file": file_path,
            "document_type": result['document_type'],
            "reason": result['reason'],
            "text": text
        }

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(process_entry, extracted_texts)
    
    # Collect results into the output list
    output = list(results)
    
    return output


        