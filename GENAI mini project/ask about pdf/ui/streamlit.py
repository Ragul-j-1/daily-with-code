import streamlit as st 
import requests
st.title("ASK ABOUT YOUR PDF")
upload_file=st.file_uploader("upload your pdf",type=["pdf"])

if upload_file is not None:
    files={
        "pdf":(
            upload_file.name,
            upload_file.getvalue(),
            "application/pdf"
        )
    }
    response=requests.post(
        "http://127.0.0.1:8000/screening/",
        files=files
    )
    if response.status_code==200:
        st.success("File processed successfully")
        st.write(response.json())
    else:
        st.error("Upload failed")
        st.text(response.text)