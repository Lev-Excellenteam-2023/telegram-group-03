from os import getenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, \
    CallbackContext


def get_bot_token():
    return getenv("DENTAL_AID_BOT_TOKEN")


# TODO create separate file to handle consts
TOKEN = get_bot_token()
FULL_NAME = 0
PHONE = 1
SYMPTOMS = 2


async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Hi! Thanks for chatting with me!\nI am the Dentist Aid Bot. Please type /help to see the available commands.")


async def open_new_chat_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Okay, before we continue, let's start with your full name please.")
    return FULL_NAME


async def get_name(update: Update, context: CallbackContext):
    user_full_name = update.message.text

    context.user_data['full_name'] = user_full_name

    await update.message.reply_text(
        "great! now can you please provide a phone number you can be reached on...")

    return 1


async def get_phone(update: Update, context: CallbackContext):
    phone = update.message.text

    context.user_data['phone'] = phone

    await update.message.reply_text(
        "please describe briefly, what are your symptoms?")

    return 2


async def get_symptoms(update: Update, context: CallbackContext):
    symptoms = update.message.text

    context.user_data['symptoms'] = symptoms

    await update.message.reply_text(
        f"Thank you, for providing your information, the office will be in contact with you.")

    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END


def is_regular_text_message(update):
    # Custom filter function to check if the message is a regular text message
    return update.message.text and not update.message.text.startswith('/')


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('openchat', open_new_chat_command)],
        states={
            FULL_NAME: [MessageHandler(filters.Text and filters.Regex(r'^(?!/)'), get_name)],
            PHONE: [MessageHandler(filters.Text and filters.Regex(r'^(?!/)') and filters.Regex(r'^\d+$'), get_phone)],
            SYMPTOMS: [MessageHandler(filters.Text and filters.Regex(r'^(?!/)'), get_symptoms)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(conv_handler)

    app.run_polling()


if __name__ == '__main__':
    main()
