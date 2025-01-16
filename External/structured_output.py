summarizer_text = [
    {
        "name": "summarizer_text",
        "description": "Generate the summary of the given text.",
        "parameters": {
            "type": "object",
            "properties": {
                "summarized_text": {
                    "type": "object",
                    "properties": {
                        "title": {  # Fixed typo from "tilte" to "title"
                            "type": "string",
                            "description": "Title of the text."
                        },
                        "summary": {
                            "type": "string",
                            "description": "Generated summary of the text."
                        }
                    },
                    "required": ["title", "summary"]  # Corrected required fields
                }
            },
            "required": [
                "summarized_text"
            ]
        }
    }
]


chat_response = [
    {
        "name": "chat_response",
        "description": "Generate the response of the given query.",
        "parameters": {
            "type": "object",
            "properties": {
                "response": {
                    "type": "string",
                    
                    "description": "Generated response to the query."
                }
            },
            "required": [
                "response"
            ]
        }
    }
]


categorization_document_generate = [
    {
        "name": "categorization_document_generate",
        "description": "Categorize the document and provide reasoning for its selection.",
        "parameters": {
            "type": "object",
            "properties": {
                "document_type": {
                    "type": "string",
                    "description": "The type of document identified.",
                    "enum": ["Invoice", "Contract", "Resume", "Purchase Order", "Legal Document", "Financial Statement", "Uncategorized"]
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for selecting the document type."
                }
            },
            "required": ["document_type", "reason"]
        }
    }
]

invoice_data_extractor = [
    {
        "name": "invoice_data_extractor",
        "description": "Extract relevant information from an invoice, including supplier and recipient details, and provide analysis for each field.",
        "parameters": {
            "type": "object",
            "properties": {
                "supplier_details": {
                    "type": "object",
                    "properties": {
                        "supplier_name": {
                            "type": "string",
                            "description": "The name of the supplier."
                        },
                        "supplier_address": {
                            "type": "string",
                            "description": "The address of the supplier."
                        },
                        "analysis": {
                            "type": "string",
                            "description": "The analysis for the supplier details."
                        },
                        "supplier_score": {
                            "type": "number",
                            "description": "The score of the supplier details field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["supplier_name", "supplier_address", "analysis", "supplier_score"]
                },
                "recipient_details": {
                    "type": "object",
                    "properties": {
                        "recipient_name": {
                            "type": "string",
                            "description": "The name of the recipient."
                        },
                        "recipient_address": {
                            "type": "string",
                            "description": "The address of the recipient."
                        },
                        "analysis": {
                            "type": "string",
                            "description": "The analysis for the recipient details."
                        },
                        "recipient_score": {
                            "type": "number",
                            "description": "The score of the recipient details field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["recipient_name", "recipient_address", "analysis", "recipient_score"]
                },
                "invoice_number": {
                    "type": "object",
                    "properties": {
                        "invoice_number": {
                            "type": "string",
                            "description": "The invoice number. If the number is not given, write None."
                        },
                        "analysis": {
                            "type": "string",
                            "description": "The analysis for the invoice number."
                        },
                        "invoice_score": {
                            "type": "number",
                            "description": "The score of the invoice number field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["invoice_number", "analysis", "invoice_score"]
                },
                "customer_name": {
                    "type": "object",
                    "properties": {
                        "customer_name": {
                            "type": "string",
                            "description": "The name of the customer (e.g., 'CROWN FINE ART')."
                        },
                        "analysis": {
                            "type": "string",
                            "description": "The analysis for the customer name and its score."
                        },
                        "customer_score": {
                            "type": "number",
                            "description": "The score of the customer name field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["customer_name", "analysis", "customer_score"]
                },
                "vat_number": {
                    "type": "object",
                    "properties": {
                        "vat_number": {
                            "type": "string",
                            "description": "The VAT number of the customer."
                        },
                        "analysis": {
                            "type": "string",
                            "description": "The analysis for the VAT number."
                        },
                        "vat_score": {
                            "type": "number",
                            "description": "The score of the VAT number field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["vat_number", "analysis", "vat_score"]
                },
                "invoice_date": {
                    "type": "object",
                    "properties": {
                        "invoice_date": {
                            "type": "string",
                            "description": "The date on the invoice (e.g., '29-AUG-2024')."
                        },
                        "analysis": {
                            "type": "string",
                            "description": "The analysis for the invoice date."
                        },
                        "date_score": {
                            "type": "number",
                            "description": "The score of the invoice date field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["invoice_date", "analysis", "date_score"]
                },
                "payment_due_date": {
                    "type": "object",
                    "properties": {
                        "payment_due_date": {
                            "type": "string",
                            "description": "The payment due date mentioned on the invoice."
                        },
                        "analysis": {
                            "type": "string",
                            "description": "The analysis for the payment due date."
                        },
                        "due_date_score": {
                            "type": "number",
                            "description": "The score of the payment due date field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["payment_due_date", "analysis", "due_date_score"]
                },
                "job_number": {
                    "type": "object",
                    "properties": {
                        "job_number": {
                            "type": "string",
                            "description": "The job number associated with the invoice."
                        },
                        "analysis": {
                            "type": "string",
                            "description": "The analysis for the job number."
                        },
                        "job_score": {
                            "type": "number",
                            "description": "The score of the job number field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["job_number", "analysis", "job_score"]
                },
                "total_amount": {
                    "type": "object",
                    "properties": {
                        "total_amount": {
                            "type": "string",
                            "description": "The total amount on the invoice in AED (e.g., '8605.00')."
                        },
                        "analysis": {
                            "type": "string",
                            "description": "The analysis for the total amount."
                        },
                        "amount_score": {
                            "type": "number",
                            "description": "The score of the total amount field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["total_amount", "analysis", "amount_score"]
                },
                "vat_amount": {
                    "type": "object",
                    "properties": {
                        "vat_amount": {
                            "type": "string",
                            "description": "The VAT amount on the invoice (e.g., '0.00')."
                        },
                        "analysis": {
                            "type": "string",
                            "description": "The analysis for the VAT amount."
                        },
                        "vat_score": {
                            "type": "number",
                            "description": "The score of the VAT amount field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["vat_amount", "analysis", "vat_score"]
                }
            },
            "required": [
                "supplier_details",
                "recipient_details",
                "invoice_number",
                "customer_name",
                "vat_number",
                "invoice_date",
                "payment_due_date",
                "job_number",
                "total_amount",
                "vat_amount"
            ]
        }
    }
]

purchase_order_data_extractor = [
    {
        "name": "purchase_order_data_extractor",
        "description": "Extract important details from a purchase order document and calculate overall score and risk.",
        "parameters": {
            "type": "object",
            "properties": {
                "purchase_order_number": {
                    "type": "object",
                    "properties": {
                        "po_number": {
                            "type": "string",
                            "description": "The purchase order number. If not found, return None."
                        },
                        "po_number_score": {
                            "type": "number",
                            "description": "The score of the purchase order number field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["po_number", "po_number_score"]
                },
                "supplier_details": {
                    "type": "object",
                    "properties": {
                        "supplier": {
                            "type": "string",
                            "description": "The name or details of the supplier."
                        },
                        "supplier_score": {
                            "type": "number",
                            "description": "The score of the supplier details field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["supplier", "supplier_score"]
                },
                "buyer_details": {
                    "type": "object",
                    "properties": {
                        "buyer": {
                            "type": "string",
                            "description": "The name or details of the buyer."
                        },
                        "buyer_score": {
                            "type": "number",
                            "description": "The score of the buyer details field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["buyer", "buyer_score"]
                },
                "order_date": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "The date the purchase order was issued. If not found, return None."
                        },
                        "order_date_score": {
                            "type": "number",
                            "description": "The score of the order date field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["date", "order_date_score"]
                },
                "delivery_date": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "The expected delivery date of the order. If not found, return None."
                        },
                        "delivery_date_score": {
                            "type": "number",
                            "description": "The score of the delivery date field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["date", "delivery_date_score"]
                },
                "item_details": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "item_name": {
                                        "type": "string",
                                        "description": "The name or description of the item."
                                    },
                                    "quantity": {
                                        "type": "number",
                                        "description": "The quantity of the item ordered."
                                    },
                                    "unit_price": {
                                        "type": "number",
                                        "description": "The unit price of the item."
                                    },
                                    "total_price": {
                                        "type": "number",
                                        "description": "The total price for the item (quantity x unit price)."
                                    }
                                },
                                "required": ["item_name", "quantity", "unit_price", "total_price"]
                            }
                        },
                        "items_score": {
                            "type": "number",
                            "description": "The score of the item details field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["items", "items_score"]
                },
                "payment_terms": {
                    "type": "object",
                    "properties": {
                        "terms": {
                            "type": "string",
                            "description": "Details of payment terms in the purchase order."
                        },
                        "terms_score": {
                            "type": "number",
                            "description": "The score of the payment terms field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["terms", "terms_score"]
                },
                "overall_score": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "number",
                            "description": "The total normalized score of the purchase order out of 10, calculated based on field scores."
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reasoning behind the overall score (e.g., which fields contributed to the score)."
                        }
                    },
                    "required": ["score", "reason"]
                },
                "overall_risk": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "number",
                            "description": "The overall risk level of the purchase order out of 10 (10 being very high risk)."
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reasoning behind the assigned risk level (e.g., which fields are missing or incomplete)."
                        }
                    },
                    "required": ["score", "reason"]
                }
            },
            "required": [
                "purchase_order_number",
                "supplier_details",
                "buyer_details",
                "order_date",
                "delivery_date",
                "item_details",
                "payment_terms",
                "overall_score",
                "overall_risk"
            ]
        }
    }
]



financial_statement_data_extractor = [
    {
        "name": "financial_statement_data_extractor",
        "description": "Extract key information from a company's financial statement and assess overall financial health.",
        "parameters": {
            "type": "object",
            "properties": {
                "balance_sheet": {
                    "type": "object",
                    "properties": {
                        "assets": {
                            "type": "object",
                            "properties": {
                                "current_assets": {
                                    "type": "number",
                                    "description": "Total current assets."
                                },
                                "non_current_assets": {
                                    "type": "number",
                                    "description": "Total non-current assets."
                                },
                                "total_assets": {
                                    "type": "number",
                                    "description": "Total assets."
                                },
                                "assets_score": {
                                    "type": "number",
                                    "description": "Score for the assets section. If complete, score is 10; otherwise, 0."
                                }
                            },
                            "required": ["current_assets", "non_current_assets", "total_assets", "assets_score"]
                        },
                        "liabilities": {
                            "type": "object",
                            "properties": {
                                "current_liabilities": {
                                    "type": "number",
                                    "description": "Total current liabilities."
                                },
                                "non_current_liabilities": {
                                    "type": "number",
                                    "description": "Total non-current liabilities."
                                },
                                "total_liabilities": {
                                    "type": "number",
                                    "description": "Total liabilities."
                                },
                                "liabilities_score": {
                                    "type": "number",
                                    "description": "Score for the liabilities section. If complete, score is 10; otherwise, 0."
                                }
                            },
                            "required": ["current_liabilities", "non_current_liabilities", "total_liabilities", "liabilities_score"]
                        },
                        "equity": {
                            "type": "number",
                            "description": "Total shareholder equity."
                        },
                        "equity_score": {
                            "type": "number",
                            "description": "Score for the equity section. If complete, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["assets", "liabilities", "equity", "equity_score"]
                },
                "income_statement": {
                    "type": "object",
                    "properties": {
                        "revenue": {
                            "type": "number",
                            "description": "Total revenue for the period."
                        },
                        "expenses": {
                            "type": "number",
                            "description": "Total expenses for the period."
                        },
                        "net_income": {
                            "type": "number",
                            "description": "Net income (profit or loss) for the period."
                        },
                        "income_statement_score": {
                            "type": "number",
                            "description": "Score for the income statement section. If complete, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["revenue", "expenses", "net_income", "income_statement_score"]
                },
                "cash_flow_statement": {
                    "type": "object",
                    "properties": {
                        "operating_cash_flow": {
                            "type": "number",
                            "description": "Cash flow from operating activities."
                        },
                        "investing_cash_flow": {
                            "type": "number",
                            "description": "Cash flow from investing activities."
                        },
                        "financing_cash_flow": {
                            "type": "number",
                            "description": "Cash flow from financing activities."
                        },
                        "net_cash_flow": {
                            "type": "number",
                            "description": "Net cash flow for the period."
                        },
                        "cash_flow_score": {
                            "type": "number",
                            "description": "Score for the cash flow statement section. If complete, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["operating_cash_flow", "investing_cash_flow", "financing_cash_flow", "net_cash_flow", "cash_flow_score"]
                },
                "ratios": {
                    "type": "object",
                    "properties": {
                        "current_ratio": {
                            "type": "number",
                            "description": "Current ratio (current assets divided by current liabilities)."
                        },
                        "debt_to_equity_ratio": {
                            "type": "number",
                            "description": "Debt-to-equity ratio (total liabilities divided by equity)."
                        },
                        "profit_margin": {
                            "type": "number",
                            "description": "Net profit margin (net income divided by revenue)."
                        },
                        "ratios_score": {
                            "type": "number",
                            "description": "Score for the ratios section. If all ratios are provided, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["current_ratio", "debt_to_equity_ratio", "profit_margin", "ratios_score"]
                },
                "overall_analysis": {
                    "type": "object",
                    "properties": {
                        "financial_health_score": {
                            "type": "number",
                            "description": "Overall financial health score out of 10."
                        },
                        "analysis_reason": {
                            "type": "string",
                            "description": "Reasoning behind the assigned financial health score."
                        }
                    },
                    "required": ["financial_health_score", "analysis_reason"]
                }
            },
            "required": [
                "balance_sheet",
                "income_statement",
                "cash_flow_statement",
                "ratios",
                "overall_analysis"
            ]
        }
    }
]


resume_data_extractor = [
    {
        "name": "resume_data_extractor",
        "description": "Extract key information from a resume and assess its overall quality.",
        "parameters": {
            "type": "object",
            "properties": {
                "personal_information": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Full name of the individual."
                        },
                        "contact_information": {
                            "type": "object",
                            "properties": {
                                "email": {
                                    "type": "string",
                                    "description": "Email address."
                                },
                                "phone": {
                                    "type": "string",
                                    "description": "Phone number."
                                },
                                "address": {
                                    "type": "string",
                                    "description": "Full address."
                                }
                            },
                            "required": ["email", "phone", "address"]
                        },
                        "personal_info_score": {
                            "type": "number",
                            "description": "Score for the personal information section. If all fields are present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["name", "contact_information", "personal_info_score"]
                },
                "employment_history": {
                    "type": "object",
                    "properties": {
                        "jobs": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "job_title": {
                                        "type": "string",
                                        "description": "Title of the job position."
                                    },
                                    "company_name": {
                                        "type": "string",
                                        "description": "Name of the company."
                                    },
                                    "duration": {
                                        "type": "string",
                                        "description": "Duration of employment."
                                    },
                                    "responsibilities": {
                                        "type": "string",
                                        "description": "Key responsibilities in the role."
                                    }
                                },
                                "required": ["job_title", "company_name", "duration", "responsibilities"]
                            }
                        },
                        "employment_score": {
                            "type": "number",
                            "description": "Score for the employment history section. If all fields are complete, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["jobs", "employment_score"]
                },
                "education": {
                    "type": "object",
                    "properties": {
                        "degrees": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "degree": {
                                        "type": "string",
                                        "description": "Name of the degree or certification."
                                    },
                                    "institution": {
                                        "type": "string",
                                        "description": "Name of the educational institution."
                                    },
                                    "graduation_year": {
                                        "type": "string",
                                        "description": "Year of graduation or completion."
                                    }
                                },
                                "required": ["degree", "institution", "graduation_year"]
                            }
                        },
                        "education_score": {
                            "type": "number",
                            "description": "Score for the education section. If all fields are complete, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["degrees", "education_score"]
                },
                "skills": {
                    "type": "object",
                    "properties": {
                        "skills_list": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "A skill listed on the resume."
                            }
                        },
                        "skills_score": {
                            "type": "number",
                            "description": "Score for the skills section. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["skills_list", "skills_score"]
                },
                "certifications": {
                    "type": "object",
                    "properties": {
                        "certifications_list": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "certification_name": {
                                        "type": "string",
                                        "description": "Name of the certification."
                                    },
                                    "certification_date": {
                                        "type": "string",
                                        "description": "Date of certification."
                                    }
                                },
                                "required": ["certification_name", "certification_date"]
                            }
                        },
                        "certifications_score": {
                            "type": "number",
                            "description": "Score for the certifications section. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["certifications_list", "certifications_score"]
                },
                "overall_analysis": {
                    "type": "object",
                    "properties": {
                        "resume_quality_score": {
                            "type": "number",
                            "description": "Overall quality score of the resume out of 10."
                        },
                        "analysis_reason": {
                            "type": "string",
                            "description": "Reasoning behind the assigned resume quality score."
                        }
                    },
                    "required": ["resume_quality_score", "analysis_reason"]
                }
            },
            "required": [
                "personal_information",
                "employment_history",
                "education",
                "skills",
                "certifications",
                "overall_analysis"
            ]
        }
    }
]


legal_document_data_extractor = [
    {
        "name": "legal_document_data_extractor",
        "description": "Extract important details from a legal document and assess its overall quality and risk.",
        "parameters": {
            "type": "object",
            "properties": {
                "document_title": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the legal document."
                        },
                        "title_score": {
                            "type": "number",
                            "description": "Score for the document title. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["title", "title_score"]
                },
                "parties_involved": {
                    "type": "object",
                    "properties": {
                        "parties": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "Names of the parties involved in the document."
                            }
                        },
                        "parties_score": {
                            "type": "number",
                            "description": "Score for the parties involved section. If all parties are present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["parties", "parties_score"]
                },
                "effective_date": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "The effective date of the document."
                        },
                        "effective_date_score": {
                            "type": "number",
                            "description": "Score for the effective date field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["date", "effective_date_score"]
                },
                "expiration_date": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "The expiration date of the document, if applicable."
                        },
                        "expiration_date_score": {
                            "type": "number",
                            "description": "Score for the expiration date field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["date", "expiration_date_score"]
                },
                "clauses": {
                    "type": "object",
                    "properties": {
                        "key_clauses": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "Key clauses mentioned in the legal document."
                            }
                        },
                        "clauses_score": {
                            "type": "number",
                            "description": "Score for the key clauses section. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["key_clauses", "clauses_score"]
                },
                "signatures": {
                    "type": "object",
                    "properties": {
                        "signatories": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "Names of the authorized signatories."
                            }
                        },
                        "signatures_score": {
                            "type": "number",
                            "description": "Score for the signatures section. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["signatories", "signatures_score"]
                },
                "jurisdiction": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The jurisdiction governing the document."
                        },
                        "jurisdiction_score": {
                            "type": "number",
                            "description": "Score for the jurisdiction field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["location", "jurisdiction_score"]
                },
                "overall_analysis": {
                    "type": "object",
                    "properties": {
                        "legal_quality_score": {
                            "type": "number",
                            "description": "Overall quality score of the legal document out of 10."
                        },
                        "analysis_reason": {
                            "type": "string",
                            "description": "Reasoning behind the assigned legal quality score."
                        }
                    },
                    "required": ["legal_quality_score", "analysis_reason"]
                }
            },
            "required": [
                "document_title",
                "parties_involved",
                "effective_date",
                "expiration_date",
                "clauses",
                "signatures",
                "jurisdiction",
                "overall_analysis"
            ]
        }
    }
]



contract_data_extractor = [
    {
        "name": "contract_data_extractor",
        "description": "Extract important details from a contract document and calculate overall score and risk.",
        "parameters": {
            "type": "object",
            "properties": {
                "contract_title": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the contract. If not found, return None."
                        },
                        "title_score": {
                            "type": "number",
                            "description": "The score of the contract title field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["title", "title_score"]
                },
                "parties_involved": {
                    "type": "object",
                    "properties": {
                        "parties": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "Names of parties involved in the contract."
                            }
                        },
                        "parties_score": {
                            "type": "number",
                            "description": "The score of the parties involved field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["parties", "parties_score"]
                },
                "effective_date": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "The effective date of the contract. If not found, return None."
                        },
                        "date_score": {
                            "type": "number",
                            "description": "The score of the effective date field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["date", "date_score"]
                },
                "expiration_date": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "The expiration date of the contract. If not found, return None."
                        },
                        "date_score": {
                            "type": "number",
                            "description": "The score of the expiration date field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["date", "date_score"]
                },
                "payment_terms": {
                    "type": "object",
                    "properties": {
                        "terms": {
                            "type": "string",
                            "description": "Details of payment terms in the contract."
                        },
                        "terms_score": {
                            "type": "number",
                            "description": "The score of the payment terms field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["terms", "terms_score"]
                },
                "scope_of_work": {
                    "type": "object",
                    "properties": {
                        "scope": {
                            "type": "string",
                            "description": "The scope of work or responsibilities mentioned in the contract."
                        },
                        "scope_score": {
                            "type": "number",
                            "description": "The score of the scope of work field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["scope", "scope_score"]
                },
                "termination_clause": {
                    "type": "object",
                    "properties": {
                        "clause": {
                            "type": "string",
                            "description": "The termination clause details."
                        },
                        "clause_score": {
                            "type": "number",
                            "description": "The score of the termination clause field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["clause", "clause_score"]
                },
                "signatures": {
                    "type": "object",
                    "properties": {
                        "signature_details": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "Names or details of authorized signatories."
                            }
                        },
                        "signatures_score": {
                            "type": "number",
                            "description": "The score of the signatures field. If present, score is 10; otherwise, 0."
                        }
                    },
                    "required": ["signature_details", "signatures_score"]
                },
                "overall_score": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "number",
                            "description": "The total normalized score of the contract out of 10, calculated based on field scores."
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reasoning behind the overall score (e.g., which fields contributed to the score)."
                        }
                    },
                    "required": ["score", "reason"]
                },
                "overall_risk": {
                    "type": "object",
                    "properties": {
                        "score": {
                            "type": "number",
                            "description": "The overall risk level of the contract out of 10 (10 being very high risk)."
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reasoning behind the assigned risk level (e.g., which fields are missing or incomplete)."
                        }
                    },
                    "required": ["score", "reason"]
                }
            },
            "required": [
                "contract_title",
                "parties_involved",
                "effective_date",
                "expiration_date",
                "payment_terms",
                "scope_of_work",
                "termination_clause",
                "signatures",
                "overall_score",
                "overall_risk"
            ]
        }
    }
]