from livekit.plugins import google
from config import GEMINI_API_KEY, MODEL

def create_llm(provider: str):
    provider = provider.lower()

    if provider == "gemini":
        return google.LLM(
            model=MODEL,
            api_key=GEMINI_API_KEY,
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")