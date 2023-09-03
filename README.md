# Dental Aid Bot

## Description

The Dental Aid Bot is a Telegram chatbot designed to assist patients in providing their symptoms and scheduling
appointments with a dentist. It uses the GPT-3.5 Turbo model for natural language processing and has Firebase
integration for data storage.

## Prerequisites

To run this project, you'll need the following prerequisites:

- Python 3.x
- Firebase Admin SDK
- OpenAI GPT-3.5 Turbo API key
- Telegram Bot API key
- ReportLab library

## Installation

1. **Clone the repository:**

    ```
    git clone https://github.com/Lev-Excellenteam-2023/telegram-group-03.git
    ```

2. **Install the required Python packages:**
   ```
   pip install -r requirements.txt
   ```

3. **Set up Firebase:**

   To set up Firebase for your Dental Aid Bot project, follow these steps to create the JSON credentials file:

     - Go to the [Firebase Console](https://console.firebase.google.com/).

     - Sign in with your Google account or create one if you don't have it already.

     - Click on "Add project" to create a new project for your Dental Aid Bot.

     - Follow the on-screen instructions to configure your project settings. You can choose any project name and region that
        you prefer.

     - Once your project is created, click on the gear icon (Project settings) in the left-hand menu.

     - In the Project settings, navigate to the "Service accounts" tab.

     -  Under "SDK setup and configuration," click on the "Generate new private key" button. This will generate a JSON file
        containing your Firebase credentials.

     - Create a folder named "private" in the top-level directory of your project.
   
     - Place the JSON file containing your Firebase credentials in the "private" folder.


4. **Set up environment variables:**

   Create a `.env` file in the project directory and add the following variables:
   + FIREBASE_CERTIFICATE_PATH=/path/to/firebase/certificate.json
   + OPENAI_API_KEY=your_openai_api_key
   + DENTAL_AID_BOT_TOKEN=your_telegram_bot_token
   + PDF_FILE_PATH=/path/to/reports (located in REPORT directory)



5. **Run the Telegram Bot:**
   ```
   cd telegram_bot
   python main.py
   ```


## Usage

- Start a chat with the Telegram Bot by sending the `/start` command.
- Initiate a new conversation with the bot using the `/NewConversation` command.
- Follow the bot's prompts to provide your name, phone number, and symptoms.
- The bot will assist in collecting information.
- Use the `/endconversation` command, to end the current conversation, and to save the details to the DB.
- Use the `/report` command to generate a report of all patients.

## File Structure

- `main.py`: Main driver for the Telegram bot.
- `DB/firebase_handler.py`: Handles Firebase database initialization and data operations.
- `REPORT/report_handler.py`: Generates PDF reports based on patient data.
- `telegram_bot.py`: Initializes and configures the Telegram bot.
- `gpt_handler.py`: Interacts with the OpenAI GPT-3.5 Turbo model for chat responses.
- `consts.py`: Contains constants and roles used in the chatbot.
- `.env`: Configuration file for environment variables.

## Features

- Telegram chatbot for dental appointment scheduling.
- Integration with OpenAI GPT-3.5 Turbo for natural language understanding.
- Firebase database for storing patient data.
- Generation of PDF reports summarizing patient information.
- Automated severity level determination based on chat history.



