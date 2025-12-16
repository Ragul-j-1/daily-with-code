from groq import Groq
from dotenv import load_dotenv
import os
from prompt import EXTRACT_PDF_INFORMATION

load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")
client= Groq(api_key=groq_api_key)

def extract_pdf_data(pdf_txt:str):
    prompt=EXTRACT_PDF_INFORMATION.format(pdf_text=pdf_txt)
    response=client.chat.completions.create(
        model=("llama-3.3-70b-versatile"),
        messages=[
            
            
            {"role":"user","content":prompt}
        ]
        )
    print(response.choices[0].message.content)
    return response.choices[0].message.content
    