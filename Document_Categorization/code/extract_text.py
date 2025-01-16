import os
import docx2txt
from bs4 import BeautifulSoup
from striprtf.striprtf import rtf_to_text
import pdfplumber
from PIL import Image
import pytesseract
import pandas as pd
from pyxlsb import open_workbook


class FileProcessingError(Exception):
    pass


class UnsupportedFileTypeError(ValueError):
    pass


class FileTextExtractor:
    def process_pdf_file(self, filepath: str) -> str:
        """Process a PDF file and extract text."""
        try:
            text = ""
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text.strip() + "\n\n"
            return text
        except Exception as e:
            raise FileProcessingError(f"Error processing PDF file: {e}")

    def process_text_file(self, filepath: str) -> str:
        """Process a text file and return its content."""
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            raise FileProcessingError(f"Error processing text file: {e}")

    def process_docx_file(self, filepath: str) -> str:
        """Process a DOCX file and extract text."""
        try:
            return docx2txt.process(filepath)
        except Exception as e:
            raise FileProcessingError(f"Error processing DOCX file: {e}")

    def process_html_file(self, filepath: str) -> str:
        """Process an HTML file and extract text."""
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
                return soup.get_text(separator="\n")
        except Exception as e:
            raise FileProcessingError(f"Error processing HTML file: {e}")

    def process_rtf_file(self, filepath: str) -> str:
        """Process an RTF file and extract text."""
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
                return rtf_to_text(content)
        except Exception as e:
            raise FileProcessingError(f"Error processing RTF file: {e}")

    def process_image_file(self, filepath: str) -> str:
        """Process an image file and extract text using OCR."""
        try:
            with Image.open(filepath) as img:
                return pytesseract.image_to_string(img)
        except Exception as e:
            raise FileProcessingError(f"Error processing image file: {e}")

    def process_csv_file(self, filepath: str) -> str:
        """Process a CSV file and return its content as plain text."""
        try:
            df = pd.read_csv(filepath)
            return df.to_string(index=False)
        except Exception as e:
            raise FileProcessingError(f"Error processing CSV file: {e}")

    def process_excel_file(self, filepath: str) -> str:
        """Process an Excel file and return its content as plain text."""
        try:
            df = pd.read_excel(filepath)
            return df.to_string(index=False)
        except Exception as e:
            raise FileProcessingError(f"Error processing Excel file: {e}")

    def process_xlsb_file(self, filepath: str) -> str:
        """Process an XLSB file, convert it to DataFrame, and return content as plain text."""
        try:
            data = []
            with open_workbook(filepath) as wb:
                for sheet_name in wb.sheets:
                    with wb.get_sheet(sheet_name) as sheet:
                        for row in sheet.rows():
                            data.append([item.v for item in row])

            # Convert data to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])  # Assumes the first row is the header
            return df.to_string(index=False)
        except Exception as e:
            raise FileProcessingError(f"Error processing XLSB file: {e}")

    FILE_PROCESSORS = {
        ".pdf": process_pdf_file,
        ".txt": process_text_file,
        ".docx": process_docx_file,
        ".html": process_html_file,
        ".htm": process_html_file,
        ".rtf": process_rtf_file,
        ".jpg": process_image_file,
        ".png": process_image_file,
        ".jpeg": process_image_file,
        ".tiff": process_image_file,
        ".csv": process_csv_file,
        ".xls": process_excel_file,
        ".xlsx": process_excel_file,
        ".xlsb": process_xlsb_file,
    }

    def extract_text_from_file(self, path: str) -> str:
        """Extract text from a file."""
        _, file_extension = os.path.splitext(path)
        file_extension = file_extension.lower()

        if file_extension not in self.FILE_PROCESSORS:
            raise UnsupportedFileTypeError(f"Unsupported file type: {file_extension}")

        processor = self.FILE_PROCESSORS[file_extension]
        return processor(self, path)


# # Example Usage
# file_extractor = FileTextExtractor()
# text = file_extractor.extract_text_from_file(
#     r"C:\Users\Rushikesh\Desktop\Hridayam\summaizer\LongRAG Enhancing Retrieval-Augmented Generation with Long-context LLMs (1).pdf"
# )
# print(text)
