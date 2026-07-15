
from datetime import datetime
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentServer, AgentSession, JobContext, Agent
from livekit.agents.llm import function_tool
from livekit.plugins import deepgram, google, elevenlabs
import livekit.plugins.silero as silero

from config import GEMINI_API_KEY, MODEL
from prompts import SYSTEM_PROMPT
from tools import (
    availability_tool,
    booking_tool,
    history_tool,
    cancel_tool,
    reschedule_tool,
)
from logger import logger
from config import ELEVEN_API_KEY
# Load environment variables
load_dotenv()


class HospitalReceptionist(Agent):
    def __init__(self, instructions: str) -> None:
        super().__init__(
            instructions=instructions,
            tools=[
                function_tool(availability_tool),
                function_tool(booking_tool),
                function_tool(history_tool),
                function_tool(cancel_tool),
                function_tool(reschedule_tool),
            ],
        )


server = AgentServer()


@server.rtc_session(agent_name="hospital-agent")
async def hospital_agent(ctx: JobContext):

    print("STEP 1")
    await ctx.connect()
    print("STEP 2")
    print("STEP 3")
    
    import json
    metadata = json.loads(ctx.room.metadata or "{}")

    language = metadata.get("language", "english")
    stt_provider = metadata.get("stt_provider", "deepgram")
    llm_provider = metadata.get("llm_provider", "gemini")

    print("Language:", language)
    print("STT:", stt_provider)
    print("LLM:", llm_provider)

    # -----------------------------
    # Speech-to-Text Provider
    # -----------------------------
    if stt_provider == "elevenlabs":
        print("Using ElevenLabs STT")
        stt = elevenlabs.STT(api_key=ELEVEN_API_KEY)
    elif stt_provider == "sarvam":
        print("Sarvam not configured. Falling back to Deepgram.")
        stt = deepgram.STT(
            model="nova-3",
            language="multi",
            smart_format=True,
            punctuate=True,
        )
    else:
        print("Using Deepgram STT")
        stt = deepgram.STT(
            model="nova-3",
            language="multi",
            smart_format=True,
            punctuate=True,
        )

    # -----------------------------
    # LLM Provider
    # -----------------------------
    if llm_provider == "gpt":
        print("GPT selected but not configured. Falling back to Gemini.")
    elif llm_provider == "claude":
        print("Claude selected but not configured. Falling back to Gemini.")

    llm = google.LLM(
        model=MODEL,
        api_key=GEMINI_API_KEY,
    )

    # -----------------------------
    # TTS Provider
    # -----------------------------
    tts = elevenlabs.TTS(
        api_key=ELEVEN_API_KEY,
        voice_id="EXAVITQu4vr4xnSDxMaL",
        model="eleven_turbo_v2_5",
    )

    session = AgentSession(
        stt=stt,
        llm=llm,
        tts=tts,
        vad=silero.VAD.load(min_silence_duration=0.3),
    )
    print("STEP 4")
    print("SESSION CREATED")

    @session.on("conversation_item_added")
    def on_conversation_item_added(event: agents.ConversationItemAddedEvent):
        item = event.item
        role = getattr(item, "role", None)
        text = getattr(item, "text_content", None)
        if role and text:
            if role == "user":
                logger.info(f"USER: {text}")
            elif role == "assistant":
                logger.info(f"AI: {text}")

    # Build dynamic prompt with current date and time
    now = datetime.now()
    instructions = f"""
{SYSTEM_PROMPT}

Today's date: {now.strftime("%Y-%m-%d")}
Current time: {now.strftime("%H:%M")}
Timezone: Asia/Kolkata
"""

    print("STARTING SESSION")
    await session.start(
        agent=HospitalReceptionist(instructions=instructions),
        room=ctx.room,
    )
    print("SESSION STARTED")

    # Removed redundant metadata read (moved up)

    language = language.lower()
    
    if language == "hindi":
        prompt_instruction = "Greet the patient warmly in Hindi. Continue the conversation primarily in Hindi. Use English terms for medical specialties if needed."
    else:
        prompt_instruction = "Greet the patient warmly in English. If the patient replies in Hindi, continue in Hindi. Otherwise continue in English."

    print("GENERATING GREETING")
    await session.generate_reply(
        instructions=prompt_instruction
    )
    print("GREETING SENT")


if __name__ == "__main__":
    agents.cli.run_app(server)
