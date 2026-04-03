from langchain_ollama import ChatOllama


def get_llm(model: str = "gpt-oss:120b-cloud", base_url: str = "http://localhost:11434"):
    """Return a ChatOllama LLM instance."""
    return ChatOllama(
        model=model,
        base_url=base_url,
    )
