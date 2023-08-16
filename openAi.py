import openai
from os import environ
from dotenv import load_dotenv
import asyncio
import constant

def get_OpenAI_API_KEY():
    load_dotenv()
    return environ.get('OpenAI_API_KEY')

openai.api_key = get_OpenAI_API_KEY()

async def get_chat_response(messages):
    response =await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message["content"]

def get_user_input():
    return input("User: ")

def exit_conversation(message):
    print(message)

def return_gpt_output(text):
    print(text)

async def create_conversation():
    conversation = [{"role": "system", "content": constant.Content}]
    while True:
        user_input = get_user_input()

        if user_input.lower() == "exit":
            exit_conversation("Chatbot: Goodbye!")
            break

        conversation.append({"role": "user", "content": user_input})

        bot_response = await get_chat_response(conversation)

        return_gpt_output("Chatbot:"+bot_response)#return  bot_response

        conversation.append({"role": "assistant", "content": bot_response})


def main():
    asyncio.run(create_conversation())

if __name__ == "__main__":
    main()