
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

from providers.stt import create_stt
from providers.llm import create_llm
from providers.tts import create_tts

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


server = AgentServer(num_idle_processes=1)


@server.rtc_session(agent_name="hospital-agent")
async def hospital_agent(ctx: JobContext):

    await ctx.connect()
    participant = await ctx.wait_for_participant()
    
    import json
    metadata = json.loads(participant.metadata or "{}")

    language = metadata.get("language", "english")
    stt_provider = metadata.get("stt_provider", "deepgram")
    llm_provider = metadata.get("llm_provider", "gemini")



    from languages import LANGUAGES
    
    lang_config = LANGUAGES.get(language, LANGUAGES["english"])
    stt_language_code = lang_config["stt"]

    # -----------------------------
    # Speech-to-Text Provider
    # -----------------------------
    stt = create_stt(stt_provider, stt_language_code)

    # -----------------------------
    # LLM Provider
    # -----------------------------
    llm = create_llm(llm_provider)

    # -----------------------------
    # TTS Provider
    # -----------------------------
    tts_provider = metadata.get("tts_provider", "sarvam")
    tts_language_code = lang_config.get("tts", "en")
    tts = create_tts(tts_provider, tts_language_code)

    vad = silero.VAD.load(min_silence_duration=0.3)

    session = AgentSession(
        stt=stt,
        llm=llm,
        tts=tts,
        vad=vad,
    )


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

    await session.start(
        agent=HospitalReceptionist(instructions=instructions),
        room=ctx.room,
    )

    # Removed redundant metadata read (moved up)

    language = language.lower()
    
    if language == "hindi":
        prompt_instruction = "Greet the patient warmly in Hindi. Continue the conversation primarily in Hindi. Use English terms for medical specialties if needed."
    else:
        prompt_instruction = "Greet the patient warmly in English. You must strictly speak ONLY in English. Do not use any Hindi words."

    await session.generate_reply(
        instructions=prompt_instruction
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
