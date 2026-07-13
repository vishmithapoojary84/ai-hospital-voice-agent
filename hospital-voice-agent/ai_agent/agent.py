from datetime import datetime
from google import genai
from google.genai import types
from logger import logger

from config import GEMINI_API_KEY, MODEL
from prompts import SYSTEM_PROMPT
from google.genai.errors import ClientError
from tools import (
    availability_tool,
    booking_tool,
    history_tool,
    cancel_tool,
    reschedule_tool,
)



client = genai.Client(
    api_key=GEMINI_API_KEY,
)


def create_chat():

    now = datetime.now()

    system_instruction = f"""
{SYSTEM_PROMPT}

Today's date: {now.strftime("%Y-%m-%d")}
Current time: {now.strftime("%H:%M")}
Timezone: Asia/Kolkata
"""

    return client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[
                availability_tool,
                booking_tool,
                history_tool,
                cancel_tool,
                reschedule_tool,
            ],
        ),
    )


chat_session = create_chat()


def chat(user_message: str):
    try:
        logger.info(f"USER: {user_message}")
        response = chat_session.send_message(
            user_message,
        )
        logger.info(f"AI: {response.text}")
        return response.text

    except ClientError as e:

        if e.code == 429:
            return (
                "I'm receiving many requests at the moment. "
                "Please wait about 20 seconds and try again."
            )

        if e.code == 503:
            return (
                "The AI service is temporarily busy. "
                "Please try again in a few moments."
            )

        raise