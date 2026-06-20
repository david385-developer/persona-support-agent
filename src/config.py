import os 
from pathlib import Path
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()



def _get_secret(key: str, default: str = "") -> str:
    """
    Read a secret from environment variables first.
    Try Streamlit secrets only as a fallback.
    """
    # Always try environment variables first
    env_value = os.getenv(key, "")
    if env_value:
        return env_value

    # Try Streamlit secrets (only works when deployed on Streamlit Cloud)
    try:
        import streamlit as st
        return st.secrets[key]
    except Exception:
        pass

    return default

@dataclass
class Config:

    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    VECTOR_STORE_DIR: Path = PROJECT_ROOT / ".vector_store"


    GROQ_API_KEY: str = field(
        default_factory=lambda: _get_secret("GROQ_API_KEY")
    )
    GROQ_MODEL: str = field(
        default_factory=lambda: _get_secret("GROQ_MODEL", "llama-3.3-70b-versatile")
    )

    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 1024

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"


    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 80
    TOP_K: int = 4
    SIMILARITY_THRESHOLD: float = 0.40

    MAX_HISTORY_TURNS: int = 10

    MAX_TURNS_BEFORE_ESACALATION: int = 4
    SENSITIVE_KEYWORDS: list = field(default_factory=lambda: [
        "billing", "refund", "charge", "legal", "lawsuit", "account deletion", "delete my account", "cancel subscription", "data breach", "hack", "hacked", "compromised", "unauthorized access", "lawyer", "attorney", "sue", "fraud",
    ])

config = Config()

