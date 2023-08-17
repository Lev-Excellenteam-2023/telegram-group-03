from os import environ
from gpt_handler import get_reply_from_chatgpt, summarize_conversions_with_gpt, get_severity_level_from_gpt
from dotenv import load_dotenv
from telegram import Update,InputFile
from telegram.ext import ConversationHandler, CallbackContext, ApplicationBuilder, CommandHandler, MessageHandler, \
    filters
from consts import FULL_NAME, PHONE, SYMPTOMS, SYSTEM_ROLE, GPT_CONVERSATION_HISTORY, \
    PATIENT_PHONE, PATIENT_SYMPTOMS, PATIENT_NAME,PDF_FILE_PATH
from DB.firebase_handler import add_record
from REPORT.report_handler import generate_report


def initialize_bot():
    app = ApplicationBuilder().token(configure_telegram_bot_api_key()).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('NewConversation', open_new_chat_command)],
        states={
            FULL_NAME: [MessageHandler(filters.Text and filters.Regex(r'^/cancel'), cancel),
                        MessageHandler(filters.Text and filters.Regex(r'^(?!/)'), get_name)],
            PHONE: [
                MessageHandler(filters.Text and filters.Regex(r'^/cancel'), cancel),
                MessageHandler(filters.Text and filters.Regex(r'^(?!/)') and filters.Regex(r'^\d+$'), get_phone)],
            SYMPTOMS: [MessageHandler(filters.Text and filters.Regex(r'^/cancel'), cancel),
                       MessageHandler(filters.Text and filters.Regex(r'^/endconversation'), end_conversation_command),
                       MessageHandler(filters.Text and filters.Regex(r'^(?!/)'), get_symptoms)]
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('restart', start_command)]
    )
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('report',export_report_command) )
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


async def restart_command(update: Update, context: CallbackContext):
    await context.bot.send_message(update.message.chat_id,
                                   "Ok!, let's start over again...")
    await start_command(update, context)
    return ConversationHandler.END


async def cancel_command(update: Update, context: CallbackContext):
    print("entered cancel")
    await context.bot.send_message(update.message.chat_id,
                                   "Oh no!😢 , I'm sorry I couldn't help you today\n if you change your mind, use /newconversation to restart the conversation")
    return ConversationHandler.END


async def end_conversation_command(update: Update, context: CallbackContext):
    await context.bot.send_message(update.message.chat_id,
                                   "Wonderful!👍🏻 Thank you for providing the information.\nWe have received your data and it's being stored super securely 🔒\nOur office will be in contact shortly to coordinate an appointment.\nHave a great day!")
    chat_summary = await summarize_conversions_with_gpt(context.user_data[GPT_CONVERSATION_HISTORY])
    severity = await get_severity_level_from_gpt(chat_summary)
    severity = [number for number in severity.split() if number.isdigit()]
    if severity == []:
        severity = 10
    else:
        severity = severity[0]
    add_record(context.user_data[PATIENT_NAME], context.user_data[PATIENT_PHONE], context.user_data[PATIENT_SYMPTOMS],
               chat_summary, int(severity))
    return ConversationHandler.END


async def export_report_command(update: Update, context: CallbackContext):
    await context.bot.send_message(update.message.chat_id,
                                   "I am exporting the report, it should appear shortly in the reports folder")
    generate_report('DoctorReport.pdf')



async def get_name(update: Update, context: CallbackContext):
    user_full_name = update.message.text

    context.user_data[PATIENT_NAME] = user_full_name

    await context.bot.send_message(update.message.chat_id,
                                   f"Thanks, {user_full_name.split()[0]}! 😊 \nNow, could you please provide a phone number where we can reach you?")

    return PHONE


async def get_phone(update: Update, context: CallbackContext):
    phone = update.message.text

    context.user_data[PATIENT_PHONE] = phone

    await context.bot.send_message(update.message.chat_id,
                                   "Awesom!. 🙌 \nCould you briefly describe the symptoms you're experiencing?")

    return SYMPTOMS


def update_gpt_history_for_user(context: CallbackContext, role: str, content: str) -> None:
    if "gpt_convo_history" not in context.user_data:
        context.user_data[GPT_CONVERSATION_HISTORY] = [{"role": "system", "content": SYSTEM_ROLE}]
        context.user_data[PATIENT_SYMPTOMS] = content
    context.user_data[GPT_CONVERSATION_HISTORY].append({"role": role, "content": content})


async def get_symptoms(update: Update, context: CallbackContext):
    user_input = update.message.text
    chat_id = update.message.chat_id

    if user_input == "/cancel":
        return ConversationHandler.END

    update_gpt_history_for_user(context, "user", user_input)
    reply = await get_reply_from_chatgpt(context.user_data["gpt_convo_history"])
    update_gpt_history_for_user(context, "assistant", reply)
    await context.bot.send_message(chat_id, reply)

    return SYMPTOMS


async def cancel(update: Update, context: CallbackContext):
    reply = await summarize_conversions_with_gpt(context)
    await update.message.reply_text(reply)
    return ConversationHandler.END
