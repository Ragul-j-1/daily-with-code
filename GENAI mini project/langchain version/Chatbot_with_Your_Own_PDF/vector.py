from langchain_community.vectorstores import FAISS



def vectorizer(documents, embedding):
    vectorstore = FAISS.from_documents(documents, embedding)
    return vectorstore
