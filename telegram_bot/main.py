from DB.firebase_handler import initialize_db
from telegram_bot import initialize_bot


def main():
    app = initialize_bot()
    initialize_db()
    app.run_polling()


if __name__ == '__main__':
    main()
