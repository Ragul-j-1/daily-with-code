from langgraph.prebuilt import chat_agent_executor



def retriver(vectorstore,llm):
    qa_chain=chat_agent_executor(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
)
    return qa_chain