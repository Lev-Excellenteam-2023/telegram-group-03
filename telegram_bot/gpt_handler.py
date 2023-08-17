from os import environ
import openai
from dotenv import load_dotenv
from consts import SUMMARIZER_ROLE, SEVERITY_LEVEL_DEFINER_ROLE
from typing import List, Dict


def configure_gpt_api_key():
    load_dotenv()
    openai.api_key = environ.get("OPEN_AI")


async def get_reply_from_chatgpt(messages_history: List[Dict[str, str]]) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_history,
    )
    return response['choices'][0]['message']['content']


async def summarize_conversions_with_gpt(messages_history: List[Dict[str, str]]) -> str:
    messages_for_prompt = [{"role": "system", "content": SUMMARIZER_ROLE}, messages_history[1:]]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_for_prompt,
    )
    return response['choices'][0]['message']['content']


async def get_severity_level_from_gpt(message_summary: str) -> str:
    messages_for_prompt = [{"role": "system", "content": SEVERITY_LEVEL_DEFINER_ROLE},
                           {"role": "user", "content": message_summary}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_for_prompt,
    )
    return response['choices'][0]['message']['content']