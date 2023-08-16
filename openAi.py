import openai
from os import environ
from dotenv import load_dotenv
import asyncio

def get_OpenAI_API_KEY():
    load_dotenv()
    return environ.get('OpenAI_API_KEY')

# Set your GPT-3.5 API key here
openai.api_key = get_OpenAI_API_KEY()

async def get_chat_response(messages):
    response =await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message["content"]

async def main():
    # Initialize a conversation with a system message
    conversation = [{"role": "system", "content": "You are a dentist who gives super short answers to your patients and wants to know about all the symptoms they have."}]

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        # Add user message to conversation
        conversation.append({"role": "user", "content": user_input})

        # Get chatbot response
        bot_response =  await get_chat_response(conversation)

        print("Chatbot:", bot_response)

        # Add chatbot message to conversation
        conversation.append({"role": "assistant", "content": bot_response})
    #show the conversation
    print(conversation)
if __name__ == "__main__":
    asyncio.run(main())