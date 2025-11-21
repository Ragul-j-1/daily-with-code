import PyPDF2 as pypdf

def parse_pdf(file) -> str:
    try:
        reader=pypdf.PdfReader(file)
        text=" "
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return str(e)        