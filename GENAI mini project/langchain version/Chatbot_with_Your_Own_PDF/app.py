import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

from pdf_loader import load_pdf
from text_spliter import chunker
from embedder import embedder
from vector import vectorizer

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=api_key,
    model="llama-3.3-70b-versatile"
)


st.set_page_config(page_title="PDF Q&A", layout="wide")
st.title("📄 Ask Questions About Your PDF")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])


def build_rag_chain(vectorstore):

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an AI assistant. Answer the question ONLY using the context below.\n\nContext:\n{context}"
        ),
        ("human", "{question}")
    ])

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    if st.button("📥 Process PDF"):
        with st.spinner("Processing PDF..."):

            documents = load_pdf(pdf_path)
            chunks = chunker(documents)
            embeddings = embedder()
            vectorstore = vectorizer(chunks, embeddings)

            st.session_state.rag_chain = build_rag_chain(vectorstore)

        st.success("PDF processed successfully!")


if "rag_chain" in st.session_state:
    question = st.text_input("Ask a question from the PDF")

    if question:
        with st.spinner("Thinking..."):
            answer = st.session_state.rag_chain.invoke(question)
            st.write("### ✅ Answer")
            st.write(answer)
