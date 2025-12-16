# Prompt for extracting PDF information
EXTRACT_PDF_INFORMATION = """
You are an AI assistant. Extract the most important information from the PDF text provided.
After analyzing the text, show the message to the user: "PDF analyzed successfully".
Provide structured JSON data if possible.
"""

# Prompt for processing user query about PDF
EXTRACT_USER_QUERY = """
You are an AI assistant. Answer the user's query based on the extracted PDF information.
Provide clear and concise answers in JSON format.
"""
