from fastapi import FastAPI, UploadFile, Form
from agents.pdf_extractor import extract_pdf_data
from agents.query_extractor import extract_query
from pdfparser import extract_pdf  # your PDF extractor function

app = FastAPI()

@app.post("/screening/")
async def screening(pdf: UploadFile, query: str = Form(...)):
    
    pdf_text = extract_pdf(pdf.file)

    
    pdf_extracted_detail = extract_pdf_data(pdf_text)

    
    user_query_details = extract_query(query,pdf_text)

    # Step 4: Return response as JSON
    return {
        "pdf_extracted_detail": pdf_extracted_detail,
        "query": query,
        "answer": user_query_details
    }
