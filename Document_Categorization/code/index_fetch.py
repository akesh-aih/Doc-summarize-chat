# from document_category.category import catgeorize_document

import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from loguru import logger
from structured_output import invoice_data_extractor,purchase_order_data_extractor,contract_data_extractor,financial_statement_data_extractor
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


def fetch_invoice_data(text,is_rlhf=False,feedback=None):

    if is_rlhf == True:
        system_content = f"""
        You are a professional invoice parser designed to extract and update important details from invoices. 
        Your task is to analyze the text, validate against RLHF feedback, and update the structured data according to the 'invoice_data_extractor' function.

        Instructions:
        - Extract details like invoice number, customer name, VAT number, invoice date, payment due date, job number, total amount, and VAT amount.
        - Validate RLHF feedback against the extracted fields:
        - If feedback is relevant to a specific field, update the value, analysis, and score based on the feedback.
        - If feedback is irrelevant to a specific field, retain the original value, analysis, and score unchanged.
        - Assign a score of 10 for a field if it is present and correct (including feedback updates, if relevant); otherwise, assign 0.
        - For fields missing in both the text and feedback, return 'None' for the value.

        IMPORTANT:
        - Use the 'invoice_data_extractor' format to generate the response.
        - Ensure the analysis for each field explicitly states:
        - Whether feedback was integrated or not.
        - Why the feedback was or was not applied.
        """

        prompt = f"""
        Analyze the provided text and RLHF feedback to extract and validate important invoice details:

        Text: {text}
        Feedback: {feedback}

        Instructions:
        1. Extract the following fields from the text:
        - Invoice number
        - Customer name
        - VAT number
        - Invoice date
        - Payment due date
        - Job number
        - Total amount
        - VAT amount
        2. Cross-check the extracted fields with RLHF feedback:
        - If feedback provides additional or corrected information for a field, update its value, analysis, and score.
        - If feedback is irrelevant to a field, retain the original extracted value, analysis, and score.
        3. For each field:
        - Return the extracted or updated value.
        - Include a detailed analysis explaining:
            - If the feedback was integrated, describe the changes and why.
            - If the feedback was not integrated, explain why it was deemed irrelevant.
        - Assign a score of 10 if the field is present and correct (including feedback updates); otherwise, assign 0.
        4. If a field is missing in both the text and feedback, return 'None' for its value.

        Output must strictly follow the 'invoice_data_extractor' format, ensuring feedback integration is accurate and well-explained.
        """



    else:
        system_content = f"""
        You are a professional invoice parser designed to extract important details from invoices. 
        Your task is to analyze the text and return structured data, as per the 'invoice_data_extractor' function.

        Ensure to identify and include:
        - Invoice number, customer name, VAT number, invoice date, payment due date, job number, total amount, and VAT amount.
        - If a field is missing in the text, return 'None' for that field.
        - Each field should include a score of 10 if present; otherwise, 0.

        Most_imp-:Use the 'invoice_data_extractor' function to generate the response.
        """

        prompt = f"""
        Analyze the following text and extract important invoice details:

        Text: {text}

        Instructions:
        1. Identify the following fields from the text: 
        - Invoice number
        - Customer name
        - VAT number
        - Invoice date
        - Payment due date
        - Job number
        - Total amount
        - VAT amount
        2. For each field, return the extracted value and a score (10 if present, 0 if not).
        3. If a field is missing, return 'None' for its value.

        Most_imp-:Output should strictly follow the 'invoice_data_extractor' format.

        Note-:Make analysis in detail.
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
            functions=invoice_data_extractor
        )

        response_message = json.loads(response.choices[0].message.function_call.arguments)
        logger.debug("Generated response successfully.")
        return response_message
        
    except Exception as e:
        logger.error(f"Error in categorizing text: {e}")
        return "An error occurred while categorizing the text."

def fetch_contract_text(text,is_rlhf=False,feedback=None):


    if is_rlhf == True:
        system_content = f"""
        You are a professional contract parser designed to extract important details from contracts and incorporate RLHF feedback when relevant. 
        Your task is to analyze the text, consider the feedback, and return structured data, as per the 'contract_data_extractor' function.

        Ensure to:
        - Extract details like contract title, parties involved, effective date, expiration date, payment terms, scope of work, termination clause, and authorized signatures.
        - Compare the RLHF feedback with the extracted text. If the feedback is relevant to a field, update the extracted value and analysis accordingly.
        - If feedback is irrelevant, keep the field's extracted value and analysis unchanged.
        - For each field, include a score of 10 if the field is present and correct (updated based on feedback if relevant); otherwise, 0.
        - Calculate the overall score of the contract out of 10 based on field scores, with a detailed reason for the score.
        - Assess the overall risk of the contract out of 10 (10 being very high risk), with a detailed reason.

        Most_IMP-:Use the 'contract_data_extractor' function to generate the response, ensuring scores and analyses are updated.
        """

        prompt = f"""
        Analyze the following text and RLHF feedback to extract and update important contract details:

        Text: {text}
        Feedback: {feedback}
        Instructions:
        1. Extract the following fields from the text:
            - Contract title
            - Parties involved
            - Effective date
            - Expiration date
            - Payment terms
            - Scope of work
            - Termination clause
            - Authorized signatures
        2. Compare the extracted fields with the RLHF feedback:
            - If the feedback provides additional or corrected information relevant to a field, update the value and analysis.
            - If the feedback is irrelevant to a field, keep the extracted value and analysis unchanged.
        3. For each field:
            - Return the extracted or updated value.
            - Include a detailed analysis explaining whether feedback was integrated or not, and why.
            - Assign a score of 10 if the field is present and correct (or updated), otherwise 0.
        4. If a field is missing in both the text and feedback, return 'None' for its value.
        5. Calculate the overall score of the contract out of 10 based on field scores, and provide a reason for the score.
        6. Assess the overall risk of the contract out of 10 (10 being very high risk), with a detailed reason.

        Most_IMP-:Output must strictly follow the 'contract_data_extractor' format, ensuring that feedback is applied correctly and analyses are detailed.
        """


    else:

        system_content = f"""
        You are a professional contract parser designed to extract important details from contracts. 
        Your task is to analyze the text and return structured data, as per the 'contract_data_extractor' function.

        Ensure to identify and include:
        - Contract title, parties involved, effective date, expiration date, payment terms, scope of work, termination clause, and authorized signatures.
        - For each field, include a score of 10 if the field is present; otherwise, 0.
        - Additionally, calculate the overall score and risk out of 10, with detailed reasons for both.

        Most_IMP-:Use the 'contract_data_extractor' function to generate the response.
        """


        prompt = f"""
        Analyze the following text and extract important contract details:

        Text: {text}

        Instructions:
        1. Identify the following fields from the text:
        - Contract title
        - Parties involved
        - Effective date
        - Expiration date
        - Payment terms
        - Scope of work
        - Termination clause
        - Authorized signatures
        2. For each field:
        - Return the extracted value.
        - Include a score (10 if present, 0 if not).
        3. If a field is missing, return 'None' for its value.
        4. Calculate the overall score of the contract out of 10 based on field scores, and provide a reason for the score.
        5. Assess the overall risk of the contract out of 10 (10 being very high risk), with a detailed reason.

        Most_IMP=Output should strictly follow the 'contract_data_extractor' format.
        Note-:Make analysis in detail.
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
            functions=contract_data_extractor
        )
        # print(response)
        response_message = json.loads(response.choices[0].message.function_call.arguments)
        logger.debug("Generated response successfully.")
        return response_message
        
    except Exception as e:
        logger.error(f"Error in categorizing text: {e}")
        return "An error occurred while categorizing the text."


def fetch_purchase_order_text(text,is_rlhf=False,feedback=None):
    if is_rlhf == True:
        system_content = f"""
        You are a professional purchase order parser designed to extract important details from purchase orders and integrate RLHF feedback when relevant. 
        Your task is to analyze the text, consider the feedback, and return structured data, as per the 'purchase_order_data_extractor' function.

        Ensure to:
        - Extract details like purchase order number, supplier details, buyer details, order date, delivery date, item details, and payment terms.
        - Compare the RLHF feedback with the extracted text. If the feedback is relevant to a field, update the extracted value and analysis accordingly.
        - If feedback is irrelevant, keep the field's extracted value and analysis unchanged.
        - For each field, include a score of 10 if the field is present and correct (updated based on feedback if relevant); otherwise, 0.
        - Calculate the overall score of the purchase order out of 10 based on field scores, with a detailed reason for the score.
        - Assess the overall risk of the purchase order out of 10 (10 being very high risk), with a detailed reason.

        IMP-:Use the 'purchase_order_data_extractor' function to generate the response, ensuring scores and analyses are updated.
        """

        prompt = f"""
        Analyze the following text and RLHF feedback to extract and update important purchase order details:

        Text: {text}
        Feedback: {feedback}
        Instructions:
        1. Extract the following fields from the text:
            - Purchase order number
            - Supplier details
            - Buyer details
            - Order date
            - Delivery date
            - Item details
            - Payment terms
        2. Compare the extracted fields with the RLHF feedback:
            - If the feedback provides additional or corrected information relevant to a field, update the value and analysis.
            - If the feedback is irrelevant to a field, keep the extracted value and analysis unchanged.
        3. For each field:
            - Return the extracted or updated value.
            - Include a detailed analysis explaining whether feedback was integrated or not, and why.
            - Assign a score of 10 if the field is present and correct (or updated), otherwise 0.
        4. If a field is missing in both the text and feedback, return 'None' for its value.
        5. Calculate the overall score of the purchase order out of 10 based on field scores, and provide a reason for the score.
        6. Assess the overall risk of the purchase order out of 10 (10 being very high risk), with a detailed reason.

        IMP-:Output must strictly follow the 'purchase_order_data_extractor' format, ensuring that feedback is applied correctly and analyses are detailed.
        """


    else:
        system_content = f"""
        You are a professional purchase order parser designed to extract important details from purchase orders. 
        Your task is to analyze the text and return structured data, as per the 'purchase_order_data_extractor' function.

        Ensure to identify and include:
        - Purchase order number, supplier details, buyer details, order date, delivery date, item details, and payment terms.
        - For each field, include a score of 10 if the field is present; otherwise, 0.
        - Additionally, calculate the overall score and risk out of 10, with detailed reasons for both.

        IMP-:SUse the 'purchase_order_data_extractor' function to generate the response.
        """

        prompt = f"""
        Analyze the following text and extract important purchase order details:

        Text: {text}

        Instructions:
        1. Identify the following fields from the text:
        - Purchase order number
        - Supplier details
        - Buyer details
        - Order date
        - Delivery date
        - Item details
        - Payment terms
        2. For each field:
        - Return the extracted value.
        - Include a score (10 if present, 0 if not).
        3. If a field is missing, return 'None' for its value.
        4. Calculate the overall score of the purchase order out of 10 based on field scores, and provide a reason for the score.
        5. Assess the overall risk of the purchase order out of 10 (10 being very high risk), with a detailed reason.

        imp-:Output should strictly follow the 'purchase_order_data_extractor' format.
        Note-:Make analysis in detail.
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
            functions=purchase_order_data_extractor
        )
        # print(response)
        response_message = json.loads(response.choices[0].message.function_call.arguments)
        logger.debug("Generated response successfully.")
        return response_message
        
    except Exception as e:
        logger.error(f"Error in categorizing text: {e}")
        return "An error occurred while categorizing the text."
    

# def financial_text(text,is_rlhf=False,feedback=None):
#     if is_rlhf == True:
#         system_content = f"""
#         You are a professional financial_text parser designed to extract important details from financial_text and incorporate RLHF feedback when relevant. 
#         Your task is to analyze the text, consider the feedback, and return structured data, as per the 'purchase_order_data_extractor' function.

#         Ensure to:
#         - Extract details like financial_text number, supplier details, buyer details, order date, delivery date, item details, and payment terms.
#         - Compare the RLHF feedback with the extracted text. If the feedback is relevant to a field, update the extracted value, analysis, and score accordingly.
#         - If feedback is irrelevant, keep the field's extracted value, analysis, and score unchanged.
#         - For each field, include a score of 10 if the field is present and correct (updated based on feedback if relevant); otherwise, 0.
#         - Calculate the overall score of the financial_text out of 10 based on field scores, with a detailed reason for the score.
#         - Assess the overall risk of the financial_text out of 10 (10 being very high risk), with a detailed reason.

#         IMP-:Use the 'financial_statement_data_extractor' function to generate the response, ensuring scores and analyses are updated where applicable.
#         """

#         prompt = f"""
#         Analyze the following text and RLHF feedback to extract and update importantfinancial_text details:

#         Text: {text}
#         Feedback: {feedback}
#         Instructions:
#         1. Extract the following fields from the text:
#             - financial_text number
#             - Supplier details
#             - Buyer details
#             - Order date
#             - Delivery date
#             - Item details
#             - Payment terms
#         2. Compare the extracted fields with the RLHF feedback:
#             - If the feedback provides additional or corrected information relevant to a field, update the value, analysis, and score.
#             - If the feedback is irrelevant to a field, keep the extracted value, analysis, and score unchanged.
#         3. For each field:
#             - Return the extracted or updated value.
#             - Include a detailed analysis explaining whether feedback was integrated or not, and why.
#             - Assign a score of 10 if the field is present and correct (or updated), otherwise 0.
#         4. If a field is missing in both the text and feedback, return 'None' for its value.
#         5. Calculate the overall score of the financial_text out of 10 based on field scores, and provide a reason for the score.
#         6. Assess the overall risk of the financial_text out of 10 (10 being very high risk), with a detailed reason.

#         Output must strictly follow the 'financial_statement_data_extractor' format, ensuring feedback is applied correctly and analyses are detailed.
#         """

#     else:
#         system_content = f"""
#         You are a professional financial_text parser designed to extract important details from financial_texts. 
#         Your task is to analyze the text and return structured data, as per the 'purchase_order_data_extractor' function.

#         Ensure to identify and include:
#         - financial_text number, supplier details, buyer details, order date, delivery date, item details, and payment terms.
#         - For each field, include a score of 10 if the field is present; otherwise, 0.
#         - Additionally, calculate the overall score and risk out of 10, with detailed reasons for both.

#         IMP-:Use the 'purchase_order_data_extractor' function to generate the response.
#         """

#         prompt = f"""
#         Analyze the following text and extract important financial_text details:

#         Text: {text}

#         Instructions:
#         1. Identify the following fields from the text:
#         - Purchase order number
#         - Supplier details
#         - Buyer details
#         - Order date
#         - Delivery date
#         - Item details
#         - Payment terms
#         2. For each field:
#         - Return the extracted value.
#         - Include a score (10 if present, 0 if not).
#         3. If a field is missing, return 'None' for its value.
#         4. Calculate the overall score of the financial_text out of 10 based on field scores, and provide a reason for the score.
#         5. Assess the overall risk of the financial_text out of 10 (10 being very high risk), with a detailed reason.

#         Output should strictly follow the 'financial_statement_data_extractor' format.
#         Note-:Make analysis in detail.
#         """




#     messages = [
#         {"role": "system", "content": system_content},
#         {"role": "user", "content": prompt}
#     ]

#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-glo-std",
#             messages=messages,
#             temperature=0.3,
#             function_call="auto",
#             functions=financial_statement_data_extractor
#         )
#         # print(response)
#         response_message = json.loads(response.choices[0].message.function_call.arguments)
#         logger.debug("Generated response successfully.")
#         return response_message
        
#     except Exception as e:
#         logger.error(f"Error in categorizing text: {e}")
#         return "An error occurred while categorizing the text."
    

def fetch_financial_statement_data(text,is_rlhf=False,feedback=None):
    if is_rlhf==True:
        system_content = f"""
You are a professional financial statement parser designed to extract important details from financial statements. 
Your task is to analyze the text and return structured data, as per the 'financial_statement_data_extractor' function.

Ensure to identify and include:
- Balance sheet (assets, liabilities, equity with scores).
- Income statement (revenue, expenses, net income with scores).
- Cash flow statement (operating, investing, financing cash flows, and net cash flow with scores).
- Ratios (current ratio, debt-to-equity ratio, profit margin with scores).
- Overall analysis (financial health score and reasoning).
- For each field, include a score of 10 if the field is present and complete; otherwise, 0.

IMP-:Use the 'financial_statement_data_extractor' function to generate the response.
"""

        prompt = f"""
    Analyze the following text and extract important financial statement details:

    Text: {text}

    Instructions:
    1. Identify the following fields from the text:
    - Balance sheet (assets, liabilities, equity).
    - Income statement (revenue, expenses, net income).
    - Cash flow statement (operating, investing, financing cash flows, and net cash flow).
    - Ratios (current ratio, debt-to-equity ratio, profit margin).
    - Overall analysis (financial health score and reasoning).
    2. For each field:
    - Return the extracted value.
    - Include a score (10 if present and complete, 0 if not).
    3. If a field is missing, return 'None' for its value.
    4. Calculate the overall financial health score out of 10 based on field scores, and provide a reason for the score.
    5. Assess the overall risk of the financial statement out of 10 (10 being very high risk), with a detailed reason.

    Output should strictly follow the 'financial_statement_data_extractor' format.
    Note-:Make analysis in detail.
    """
    else:
        system_content = f"""
    You are a professional financial statement parser designed to extract important details from financial statements. 
    Your task is to analyze the text and return structured data, as per the 'financial_statement_data_extractor' function.

    Ensure to identify and include:
    - Balance sheet (assets, liabilities, equity with scores).
    - Income statement (revenue, expenses, net income with scores).
    - Cash flow statement (operating, investing, financing cash flows, and net cash flow with scores).
    - Ratios (current ratio, debt-to-equity ratio, profit margin with scores).
    - Overall analysis (financial health score and reasoning).
    - For each field, include a score of 10 if the field is present and complete; otherwise, 0.

    IMP-:Use the 'financial_statement_data_extractor' function to generate the response.
    """

        prompt = f"""
        Analyze the following text and extract important financial statement details:

        Text: {text}

        Instructions:
        1. Identify the following fields from the text:
        - Balance sheet (assets, liabilities, equity).
        - Income statement (revenue, expenses, net income).
        - Cash flow statement (operating, investing, financing cash flows, and net cash flow).
        - Ratios (current ratio, debt-to-equity ratio, profit margin).
        - Overall analysis (financial health score and reasoning).
        2. For each field:
        - Return the extracted value.
        - Include a score (10 if present and complete, 0 if not).
        3. If a field is missing, return 'None' for its value.
        4. Calculate the overall financial health score out of 10 based on field scores, and provide a reason for the score.
        5. Assess the overall risk of the financial statement out of 10 (10 being very high risk), with a detailed reason.

        Output should strictly follow the 'financial_statement_data_extractor' format.
        Note-:Make analysis in detail.
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
            functions=financial_statement_data_extractor
        )
        # print(response)
        response_message = json.loads(response.choices[0].message.function_call.arguments)
        logger.debug("Generated response successfully.")
        return response_message
        
    except Exception as e:
        logger.error(f"Error in categorizing text: {e}")
        return "An error occurred while categorizing the text."


def fetch_resume_text(text,is_rlhf=False,feedback=None):
    if is_rlhf == True:
        system_content = f"""
        You are a professional resume parser designed to extract important details from resumes and integrate RLHF feedback when relevant.
        Your task is to analyze the text, consider the feedback, and return structured data, as per the 'resume_data_extractor' function.

        Ensure to:
        - Extract details like personal information (name, contact details), employment history (job title, company, duration, responsibilities), 
        education (degrees, institutions, graduation years), skills (list of skills), and certifications (certification name, date).
        - Compare the RLHF feedback with the extracted text. If the feedback is relevant to a field, update the extracted value, analysis, and score accordingly.
        - If feedback is irrelevant, keep the field's extracted value, analysis, and score unchanged.
        - For each field, include a score of 10 if the field is present and complete (updated based on feedback if relevant); otherwise, 0.
        - Calculate the overall resume quality score out of 10 based on field scores, with a detailed reason for the score.
        - Assess the overall quality and completeness of the resume, with a detailed reasoning.

        IMP-:Use the 'resume_data_extractor' function to generate the response, ensuring feedback is applied correctly where relevant.
        """

        prompt = f"""
        Analyze the following text and RLHF feedback to extract and update important resume details:

        Text: {text}
        Feedback: {feedback}

        Instructions:
        1. Extract the following fields from the text:
            - Personal information (name, contact details).
            - Employment history (job title, company, duration, responsibilities).
            - Education (degrees, institutions, graduation years).
            - Skills (list of skills).
            - Certifications (certification name, date).
        2. Compare the extracted fields with the RLHF feedback:
            - If the feedback provides additional or corrected information relevant to a field, update the value, analysis, and score.
            - If the feedback is irrelevant to a field, keep the extracted value, analysis, and score unchanged.
        3. For each field:
            - Return the extracted or updated value.
            - Include a detailed analysis explaining whether feedback was integrated or not, and why.
            - Assign a score of 10 if the field is present and complete (or updated), otherwise 0.
        4. If a field is missing in both the text and feedback, return 'None' for its value.
        5. Calculate the overall resume quality score out of 10 based on field scores, and provide a reason for the score.
        6. Assess the overall quality and completeness of the resume, with a detailed reasoning.

        Output must strictly follow the 'resume_data_extractor' format, ensuring that feedback is applied correctly and analyses are detailed.
        """


    else:

        system_content = f"""
        You are a professional resume parser designed to extract important details from resumes. 
        Your task is to analyze the text and return structured data, as per the 'resume_data_extractor' function.

        Ensure to identify and include:
        - Personal information (name, contact details with scores).
        - Employment history (job title, company, duration, responsibilities with scores).
        - Education (degrees, institutions, graduation years with scores).
        - Skills (list of skills with scores).
        - Certifications (certification name, date with scores).
        - Overall analysis (resume quality score and reasoning).
        - For each field, include a score of 10 if the field is present and complete; otherwise, 0.

        IMP-:Use the 'resume_data_extractor' function to generate the response.
        """

        prompt = f"""
        Analyze the following text and extract important resume details:

        Text: {text}

        Instructions:
        1. Identify the following fields from the text:
        - Personal information (name, contact details).
        - Employment history (job title, company, duration, responsibilities).
        - Education (degrees, institutions, graduation years).
        - Skills (list of skills).
        - Certifications (certification name, date).
        2. For each field:
        - Return the extracted value.
        - Include a score (10 if present and complete, 0 if not).
        3. If a field is missing, return 'None' for its value.
        4. Calculate the overall resume quality score out of 10 based on field scores, and provide a reason for the score.
        5. Assess the overall quality and completeness of the resume, with a detailed reasoning.

        Output should strictly follow the 'resume_data_extractor' format.
        Note-:Make analysis in detail.
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
            functions=financial_statement_data_extractor
        )
        # print(response)
        response_message = json.loads(response.choices[0].message.function_call.arguments)
        logger.debug("Generated response successfully.")
        return response_message
        
    except Exception as e:
        logger.error(f"Error in categorizing text: {e}")
        return "An error occurred while categorizing the text."

def fetch_legal_document_text(text,is_rlhf=False,feedback=None):
    if is_rlhf == True:
        system_content = f"""
        You are a professional legal document parser designed to extract important details from legal documents and incorporate RLHF feedback when relevant.
        Your task is to analyze the text, consider the feedback, and return structured data, as per the 'legal_document_data_extractor' function.

        Ensure to:
        - Extract details like document title, parties involved, effective date, expiration date, key clauses, signatures, and jurisdiction.
        - Compare the RLHF feedback with the extracted text. If the feedback is relevant to a field, update the extracted value, analysis, and score accordingly.
        - If feedback is irrelevant, keep the field's extracted value, analysis, and score unchanged.
        - For each field, include a score of 10 if the field is present and complete (updated based on feedback if relevant); otherwise, 0.
        - Calculate the overall legal document quality score out of 10 based on field scores, with a detailed reason for the score.
        - Assess the overall quality and risk of the legal document, with a detailed reasoning.

        IMP-:Use the 'legal_document_data_extractor' function to generate the response, ensuring feedback is applied correctly where relevant.
        """

        prompt = f"""
        Analyze the following text and RLHF feedback to extract and update important legal document details:

        Text: {text}
        Feedback: {feedback}

        Instructions:
        1. Extract the following fields from the text:
            - Document title (title).
            - Parties involved (list of parties).
            - Effective date and expiration date (dates).
            - Key clauses (list of clauses).
            - Signatures (list of signatories).
            - Jurisdiction (governing location).
        2. Compare the extracted fields with the RLHF feedback:
            - If the feedback provides additional or corrected information relevant to a field, update the value, analysis, and score.
            - If the feedback is irrelevant to a field, keep the extracted value, analysis, and score unchanged.
        3. For each field:
            - Return the extracted or updated value.
            - Include a detailed analysis explaining whether feedback was integrated or not, and why.
            - Assign a score of 10 if the field is present and complete (or updated), otherwise 0.
        4. If a field is missing in both the text and feedback, return 'None' for its value.
        5. Calculate the overall legal document quality score out of 10 based on field scores, and provide a reason for the score.
        6. Assess the overall quality and risk of the legal document, with a detailed reasoning.

        Output must strictly follow the 'legal_document_data_extractor' format, ensuring feedback is applied correctly and analyses are detailed.
        """


    else:
        system_content = f"""
        You are a professional legal document parser designed to extract important details from legal documents. 
        Your task is to analyze the text and return structured data, as per the 'legal_document_data_extractor' function.

        Ensure to identify and include:
        - Document title (title with score).
        - Parties involved (list of parties with score).
        - Effective date and expiration date (dates with scores).
        - Key clauses (list of clauses with score).
        - Signatures (list of signatories with score).
        - Jurisdiction (governing location with score).
        - Overall analysis (legal quality score and reasoning).
        - For each field, include a score of 10 if the field is present and complete; otherwise, 0.

        IMp-:Use the 'legal_document_data_extractor' function to generate the response.
        """


        prompt = f"""
        Analyze the following text and extract important legal document details:

        Text: {text}

        Instructions:
        1. Identify the following fields from the text:
        - Document title (title).
        - Parties involved (list of parties).
        - Effective date and expiration date (dates).
        - Key clauses (list of clauses).
        - Signatures (list of signatories).
        - Jurisdiction (governing location).
        2. For each field:
        - Return the extracted value.
        - Include a score (10 if present and complete, 0 if not).
        3. If a field is missing, return 'None' for its value.
        4. Calculate the overall legal document quality score out of 10 based on field scores, and provide a reason for the score.
        5. Assess the overall quality and risk of the legal document, with a detailed reasoning.

        Output should strictly follow the 'legal_document_data_extractor' format.
        Note-:Make analysis in detail.
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
            functions=financial_statement_data_extractor
        )
        # print(response)
        response_message = json.loads(response.choices[0].message.function_call.arguments)
        logger.debug("Generated response successfully.")
        return response_message
        
    except Exception as e:
        logger.error(f"Error in categorizing text: {e}")
        return "An error occurred while categorizing the text."






def index_fetch(document_type,text,is_rlhf,feedback_intent):
    # input("-----> Press Enter to continue <-----")
    if document_type=='Invoice':
        inovoice_output=fetch_invoice_data(text,is_rlhf=is_rlhf,feedback=feedback_intent)
        # print(inovoice_output)
        # input("--->")
        return inovoice_output
    elif document_type=='Contract':
        contract_data=fetch_contract_text(text,is_rlhf=is_rlhf,feedback=feedback_intent)
        return contract_data
    elif document_type=='Resume':
        Resume_data=fetch_resume_text(text,is_rlhf=is_rlhf,feedback=feedback_intent)

        return Resume_data
    elif document_type=='Purchase Order':
        purchase_data=fetch_purchase_order_text(text,is_rlhf=is_rlhf,feedback=feedback_intent)
        return purchase_data
        # return 'Purchase Order'
    elif document_type=='Legal Document':
        Legal_document_data=fetch_legal_document_text(text,is_rlhf=is_rlhf,feedback=feedback_intent)
        return 'Legal Document'
    elif document_type=='Financial Statement':
        financial_document_data=fetch_financial_statement_data(text,is_rlhf=is_rlhf,feedback=feedback_intent)
        return financial_document_data
        # return 'Financial Statement'
    else:
        return None
