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
