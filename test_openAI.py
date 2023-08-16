import asynctest
from unittest.mock import patch
from io import StringIO
from openAi import get_chat_response, create_conversation

class TestChatbotConversation(asynctest.TestCase):

    @patch("builtins.input", side_effect=["Hello", "exit"])
    @patch("sys.stdout", new_callable=StringIO)
    async def test_create_conversation(self, mock_stdout, mock_input):
        await create_conversation()
        output = mock_stdout.getvalue()
        self.assertIn("Chatbot:", output)
        self.assertIn("Goodbye!", output)

    async def test_get_chat_response(self):
        messages = [
            {"role": "system", "content": "System message"},
            {"role": "user", "content": "Hello"}
        ]
        response = await get_chat_response(messages)
        self.assertIsInstance(response, str)  # Check if the response is a string

if __name__ == "__main__":
    asynctest.main()
