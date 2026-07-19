from livekit.plugins import deepgram, elevenlabs, sarvam
from config import ELEVEN_API_KEY, SARVAM_API_KEY

def create_stt(provider: str, language: str):
    provider = provider.lower()

    if provider == "deepgram":
        return deepgram.STT(
            model="nova-3",
            language=language,
            smart_format=True,
            punctuate=True,
        )

    elif provider == "elevenlabs":
        return elevenlabs.STT(
            api_key=ELEVEN_API_KEY,
        )

    elif provider == "sarvam":
        # Sarvam expects language codes like 'en-IN', 'hi-IN'
        sarvam_lang = f"{language}-IN" if len(language) == 2 else language
        return sarvam.STT(
            api_key=SARVAM_API_KEY,
            language=sarvam_lang
        )

    else:
        raise ValueError(f"Unsupported STT provider: {provider}")