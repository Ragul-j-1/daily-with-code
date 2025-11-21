import streamlit as st
import requests

st.title("Resume Screening App")

upload_file = st.file_uploader("Upload your resume", type="pdf")

if upload_file is not None:
    st.success(f"Resume file uploaded successfully: {upload_file.name}")

    if st.button("Process resume"):

        # Read uploaded file bytes
        file_bytes = upload_file.read()

        # Send to FastAPI backend
        response = requests.post(
            "http://127.0.0.1:8000/screening/",
            files={"resume": (upload_file.name, file_bytes, "application/pdf")}
        )

        # Show response
        if response.status_code == 200:
            st.success("Resume processed successfully!")

            try:
                response_data = response.json()
                st.write("Candidate Status:", response_data.get("candidate_status"))
                st.write("Response:", response_data)
            except:
                st.error("Error: API did not return valid JSON")
                st.write(response.text)

        else:
            st.error(f"API Error: {response.status_code}")
            st.write(response.text)
