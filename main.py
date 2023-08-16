from telegram.ext import ApplicationBuilder, ConversationHandler, CommandHandler, MessageHandler, filters

from consts import FULL_NAME, PHONE, SYMPTOMS
from telegram_bot import open_new_chat_command, get_name, get_phone, get_symptoms, cancel, start_command, \
    configure_telegram_bot_api_key


def main():
    app = ApplicationBuilder().token(configure_telegram_bot_api_key()).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('openchat', open_new_chat_command)],
        states={
            FULL_NAME: [MessageHandler(filters.Text and filters.Regex(r'^(?!/)'), get_name)],
            PHONE: [MessageHandler(filters.Text and filters.Regex(r'^(?!/)') and filters.Regex(r'^\d+$'), get_phone)],
            SYMPTOMS: [MessageHandler(filters.Text and filters.Regex(r'^(?!/)'), get_symptoms)]
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('start', start_command)]
    )

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(conv_handler)

    app.run_polling()


if __name__ == '__main__':
    main()
