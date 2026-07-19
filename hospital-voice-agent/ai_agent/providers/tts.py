from livekit.plugins import elevenlabs, sarvam
from config import ELEVEN_API_KEY, SARVAM_API_KEY, ELEVEN_VOICE_ID, SARVAM_VOICE_ID

def create_tts(provider: str, language: str = "en"):
    provider = provider.lower()

    if provider == "elevenlabs":
        return elevenlabs.TTS(
            api_key=ELEVEN_API_KEY,
            voice_id=ELEVEN_VOICE_ID,
            model="eleven_turbo_v2_5",
        )

    elif provider == "sarvam":
        sarvam_lang = f"{language}-IN" if len(language) == 2 else language
        return sarvam.TTS(
            api_key=SARVAM_API_KEY,
            speaker=SARVAM_VOICE_ID,
            target_language_code=sarvam_lang,
            model="bulbul:v3"
        )

    else:
        raise ValueError(f"Unsupported TTS provider: {provider}")