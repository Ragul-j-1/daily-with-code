from groq import Groq
from prompt import EXTRACT_USER_QUERY
from dotenv import load_dotenv
import os
load_dotenv()
from agents.pdf_extractor import extract_pdf_data
GROQ_API_KEY=os.getenv("GROQ_API_KEY")


client = Groq(api_key=GROQ_API_KEY)  

def extract_query(user_query: str,pdf_text:str):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  
        messages=[
            {"role": "system", "content": pdf_text},
            {"role": "user", "content": user_query}
        ],
    )
    return response.choices[0].message.content
