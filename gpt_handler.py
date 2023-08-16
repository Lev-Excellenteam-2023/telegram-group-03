from os import environ
import openai
from dotenv import load_dotenv
from telegram.ext import CallbackContext

from consts import SUMMARIZER_ROLE


def configure_gpt_api_key():
    load_dotenv()
    openai.api_key = environ.get("OPEN_AI")


async def get_reply_from_chatgpt(context: CallbackContext) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context.user_data["gpt_convo_history"],
    )
    return response['choices'][0]['message']['content']


async def summarize_conversions_with_gpt(context: CallbackContext) -> str:
    messages = [{"role": "system", "content": SUMMARIZER_ROLE}, context.user_data["gpt_convo_history"][1:]]
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=context.user_data["gpt_convo_history"],
    )
    return response['choices'][0]['message']['content']