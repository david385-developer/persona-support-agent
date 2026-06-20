from langchain_groq import ChatGroq
from .config import config

def get_llm(temperature: float = None, max_tokens: int = None):

    return ChatGroq(
        model=config.GROQ_MODEL,
        api_key=config.GROQ_API_KEY,
        temperature=temperature if temperature is not None else config.LLM_TEMPERATURE,
        max_tokens = max_tokens or config.LLM_MAX_TOKENS
    )