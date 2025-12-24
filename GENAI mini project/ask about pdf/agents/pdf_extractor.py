from groq import Groq
from prompt import EXTRACT_PDF_INFORMATION
from dotenv import load_dotenv
import os
load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")


client = Groq(api_key=GROQ_API_KEY)  

def extract_pdf_data(pdf_text: str):
    prompt=EXTRACT_PDF_INFORMATION.format(pdf_text=pdf_text)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  
        messages=[
            {"role":"system" , "content":prompt},
            
            
        ]
    )
    
    return response.choices[0].message.content
