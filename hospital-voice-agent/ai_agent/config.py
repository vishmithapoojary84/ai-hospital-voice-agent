import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
BACKEND_URL = os.getenv("BACKEND_URL", "")
MODEL = os.getenv("GEMINI_MODEL", "")

LIVEKIT_URL = os.getenv("LIVEKIT_URL", "")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "")

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "")

ELEVEN_API_KEY=os.getenv("ELEVEN_API_KEY","")
ELEVEN_VOICE_ID=os.getenv("ELEVEN_VOICE_ID","EXAVITQu4vr4xnSDxMaL")
SARVAM_API_KEY=os.getenv("SARVAM_API_KEY", "")
SARVAM_VOICE_ID=os.getenv("SARVAM_VOICE_ID", "kavya")
