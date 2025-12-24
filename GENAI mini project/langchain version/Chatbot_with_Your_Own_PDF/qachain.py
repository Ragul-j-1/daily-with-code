
from langgraph.prebuilt import chat_agent_executor

def chains(llm,vectorstore):
    qa_chain =chat_agent_executor.from_chain_type(
        llm=llm,
        retriver=vectorstore.as_retriver(),
        return_source_documents=True
        )
    return qa_chain
