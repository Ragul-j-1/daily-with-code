from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def retriver(vectorstore, llm):
    retriever = vectorstore.as_retriever()

    prompt = ChatPromptTemplate.from_template(
        """Answer the question using the context below.
        Context: {context}
        Question: {question}
        """
    )

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
