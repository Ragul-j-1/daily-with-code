from langchain_community.embeddings import HuggingFaceEmbeddings

def embedder(document):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
