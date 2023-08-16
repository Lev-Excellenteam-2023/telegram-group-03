from os import environ
from gpt_handler import get_reply_from_chatgpt, summarize_conversions_with_gpt
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext, ApplicationBuilder, CommandHandler, MessageHandler, \
    filters
from consts import FULL_NAME, PHONE, SYMPTOMS, SYSTEM_ROLE


def initialize_bot():
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
    return app


def configure_telegram_bot_api_key():
    load_dotenv()
    return environ.get("DENTAL_AID_BOT_TOKEN")


async def start_command(update: Update, context: CallbackContext):
    await context.bot.send_message(update.message.chat_id,
                                   "Hi there! I am Dentist Aid Bot, here to help you. Thanks for chatting with me! "
                                   "If you need assistance, just type \\help.")


async def open_new_chat_command(update: Update, context: CallbackContext):
    await context.bot.send_message(update.message.chat_id,
                                   "To assist you better, could you please provide your full name?")
    return FULL_NAME


async def get_name(update: Update, context: CallbackContext):
    user_full_name = update.message.text

    context.user_data['full_name'] = user_full_name

    await context.bot.send_message(update.message.chat_id,
                                   f"Thanks, {user_full_name.split()[0]}! 😊 \nNow, could you please provide a phone number where we can reach you?")

    return PHONE


async def get_phone(update: Update, context: CallbackContext):
    phone = update.message.text

    context.user_data['phone'] = phone

    await context.bot.send_message(update.message.chat_id,
                                   "Awesom!. 🙌 \nCould you briefly describe the symptoms you're experiencing?")

    return SYMPTOMS


def update_gpt_history_for_user(context: CallbackContext, role: str, content: str) -> None:
    if "gpt_convo_history" not in context.user_data:
        context.user_data["gpt_convo_history"] = [{"role": "system", "content": SYSTEM_ROLE}]
    context.user_data["gpt_convo_history"].append({"role": role, "content": content})


async def get_symptoms(update: Update, context: CallbackContext):
    user_input = update.message.text
    chat_id = update.message.chat_id

    if user_input == "/cancel":
        return ConversationHandler.END

    update_gpt_history_for_user(context, "user", user_input)
    reply = await get_reply_from_chatgpt(context)
    update_gpt_history_for_user(context, "assistant", reply)
    await context.bot.send_message(chat_id, reply)

    return SYMPTOMS


async def cancel(update: Update, context: CallbackContext):
    reply = await summarize_conversions_with_gpt(context)
    await update.message.reply_text(reply)
    return ConversationHandler.END
