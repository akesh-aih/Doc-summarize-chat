from aih_automaton.ai_models.azure_openai_vision import AzureOpenAIVisionModel
from aih_automaton.ai_models.whisper_ai import AzureOpenAIAudioModel
from aih_rag.llms.openai_utils import ChatMessage
from aih_automaton import Agent, Task, LinearSyncPipeline
from aih_automaton.tasks.task_literals import OutputType
import pdfplumber
from typing import List, Dict
import os
from dotenv import load_dotenv
import base64
from openai import AzureOpenAI
from aih_automaton.ai_models.model_base import AIModel
from rich import print

load_dotenv()

azure_api_key = os.getenv("API_Key")
azure_endpoint = os.getenv("End_point")
azure_api_version = os.getenv('API_version')
azure_engine = os.getenv('Engine')
client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=azure_api_key,
    api_version=azure_api_version
)
# from aih_automaton import Agent, Task, LinearSyncPipeline


def find_file_recursively(file_name, search_directory):
    """Search for a file recursively in all subdirectories."""
    for root, dirs, files in os.walk(search_directory):
        if file_name in files:
            return os.path.join(root, file_name)
    raise FileNotFoundError(
        f"The file {file_name} was not found in {search_directory} or its subdirectories.")



def read_pdf(path):
    """ 
    Returns text of pdf
    """
    try:
        if path.endswith('.pdf'):
            with pdfplumber.open(path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
        else:
            raise "Provided file is not a pdf, Please provide file with .pdf extension"
    except Exception as e:
        print(f'Error :{e}')


def read_pdfs_text(pdf_names: List, search_directory=None):
    """
    Returns list of text of pdf's provided
    """
    if search_directory is None:
        search_directory = os.getcwd()
    pdf_text_list = []
    for pdf_name in pdf_names:
        # print(pdf_name.endswith('.pdf'))
        pdf_path = find_file_recursively(pdf_name, search_directory)
        pdf_text_list.append(read_pdf(pdf_path))
    return pdf_text_list



def create_text_extraction_pipeline(image_path):
    # print('\n Extracting text from image \n')

    try: 
        if image_path.endswith('.png') or image_path.endswith('.jpeg') or image_path.endswith('.jpg') or image_path.endswith('.webp') or image_path.endswith('.gif'):
            # input("--->")
            system_persona = """You are a expert in understanding Screenshots. You will be Extracting Text from images,

            Make sure Text is Structured, understandable, detailed and clear.

            Give summary of extracted text

            """


            prompt_persona = 'Extract the Text from attached files i.e.'
            text_extraction_agent = Agent(
                role='Text extraction agent',
                prompt_persona=prompt_persona
                )
            text_extraction_task = Task(
                model=AzureOpenAIVisionModel(azure_api_key=azure_api_key,
                                            engine='gpt-4-turbo-vision',
                                            azure_api_version=azure_api_version,
                                            azure_endpoint=azure_endpoint),  
                file_paths=[image_path],
                output_type=OutputType.EXTRACT,
                agent=text_extraction_agent,
                instructions=system_persona
            )
            pipeline = LinearSyncPipeline(
            tasks = [text_extraction_task],
            completion_message='\n Text Extracted Successfully\n'
            )
        else:
            raise "Image not given in proper format: We only support [.png, .jpeg, .jpg, .webp, .gif]"
    except Exception as e:
        print(f"Error: {e}")
        return None
    return pipeline


