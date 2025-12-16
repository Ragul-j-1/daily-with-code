import streamlit as st
import requests

st.set_page_config(page_title="Ask About Your PDF", layout="centered")

# ----------------------------
# Session state
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "upload"

if "pdf_file" not in st.session_state:
    st.session_state.pdf_file = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# PAGE 1: Upload PDF
# ----------------------------
if st.session_state.page == "upload":

    st.title("📄 Ask About Your PDF")

    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type=["pdf"]
    )

    if uploaded_file:
        st.session_state.pdf_file = uploaded_file
        st.success("PDF uploaded successfully ✅")

        if st.button("💬 Ask your query"):
            st.session_state.page = "chat"
            st.rerun()

# ----------------------------
# PAGE 2: Chat Page
# ----------------------------
elif st.session_state.page == "chat":

    st.title("🤖 Ask Your Query")

    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    user_query = st.chat_input("Ask something about your PDF...")

    if user_query:
        # Add user message to session
        st.session_state.messages.append({
            "role": "user",
            "content": user_query
        })

        with st.chat_message("user"):
            st.markdown(user_query)

        # ----------------------------
        # Send PDF + query to FastAPI
        # ----------------------------
        files = {
            "pdf": (
                st.session_state.pdf_file.name,
                st.session_state.pdf_file.getvalue(),
                "application/pdf"
            )
        }

        data = {
            "query": user_query
        }

        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/screening/",
                    files=files,
                    data=data
                )
                response.raise_for_status()

                assistant_reply = response.json()
                # Only show the LLM answer
                assistant_reply_text = assistant_reply.get("answer", "No answer received")

            except requests.exceptions.RequestException as e:
                assistant_reply_text = f"❌ Error from backend: {e}"

        # Add assistant message to session
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_reply_text
        })

        with st.chat_message("assistant"):
            st.markdown(assistant_reply_text)

    # Button to go back and upload another PDF
    if st.button("🔄 Upload another PDF"):
        st.session_state.page = "upload"
        st.session_state.pdf_file = None
        st.session_state.messages = []
        st.rerun()
