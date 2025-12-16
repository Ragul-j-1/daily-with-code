import pdfplumber as pp

def extract_pdf(pdf_file)->str:
       with pp.open(pdf_file) as pdf:
           text=" "
           for page in pdf.pages:
            text+=page.extract_text() +"\n"
       return text.strip()
