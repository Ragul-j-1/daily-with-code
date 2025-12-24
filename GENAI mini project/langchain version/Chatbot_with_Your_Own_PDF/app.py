import streamlit as st
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import tempfile
from pdf_loader import load_pdf
from text_spliter import chunker
from embedder import embedder
from vector import vectorizer
from retriver import retriver
load_dotenv()

api_key=os.getenv("GROQ_API_KEY")

llm=ChatGroq(api_key=api_key,model="llama-3.3-70b-versatile")

import streamlit as st

st.title("ask about you pdf")

upload_file=st.file_uploader("upload yourpdf",type=['pdf'])
if upload_file:
    with tempfile.NamedTemporaryFile(delete=False,suffix='.pdf') as temp:
        temp.write(upload_file.read())
        temp_path=temp.name

    if st.button("Process file"):
        
        load=load_pdf(temp_path)
        
        chunks=chunker(load)
        
        embed=embedder(chunks)
        
        vector=vectorizer(chunks,embed)
        
        qa_chain=retriver(vector,llm)
        user_input=st.text_input("enter your query")
        response=qa_chain.invoke({'query':user_input}) 

        if response:
            st.write(response)
            
        
        