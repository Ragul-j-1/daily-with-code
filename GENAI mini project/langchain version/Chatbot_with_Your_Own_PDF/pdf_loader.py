from langchain_community.document_loaders import PyPDFLoader

def load_pdf(temp_path):
    # converting pdf to document
    loader = PyPDFLoader(temp_path)
    documents = loader.load()
    return documents
