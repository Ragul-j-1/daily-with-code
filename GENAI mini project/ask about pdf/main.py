from fastapi import FastAPI,UploadFile
from agents.pdf_extractor import extract_pdf_data
from pdfparser import extract_pdf

app=FastAPI()

@app.post("/screening/")
async def screening(pdf:UploadFile):
    pdf_text=extract_pdf(pdf.file)
    pdf_extracted_detail=extract_pdf_data(pdf_text)
    print(pdf_extracted_detail)
    return pdf_extracted_detail