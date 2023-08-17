import openai
from os import environ
from dotenv import load_dotenv
import asyncio
import consts

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

async def summary_gpt_conversation(conversation):
    # convert the conversation to a string
    conversation_string = ""
    for message in conversation[1:]:
        conversation_string += message["role"] + ": " + message["content"] + "\n"
    conversation_string += "return me a summary of the conversation"
    # get the summary from GPT-3

    response = await openai.Completion.acreate(
            engine="text-davinci-003",  # You can adjust the engine
            prompt=conversation_string,
            max_tokens=150  # Adjust the max_tokens as needed for summary length
        )
    print("Summary: " + response.choices[0].text.strip())



async def create_conversation():
    conversation = [{"role": "system", "content": consts.Content}]
    while True:
        user_input = get_user_input()

        if user_input.lower() == "exit":
            exit_conversation("Chatbot: Goodbye!")
            break

        conversation.append({"role": "user", "content": user_input})

        bot_response = await get_chat_response(conversation)

        return_gpt_output("Chatbot:"+bot_response)#return  bot_response

        conversation.append({"role": "assistant", "content": bot_response})
    summary = await summary_gpt_conversation(conversation)

def main():
    asyncio.run(create_conversation())

if __name__ == "__main__":
    main()