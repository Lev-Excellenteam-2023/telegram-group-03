from telegram_bot import initialize_bot


def main():
    app = initialize_bot()
    app.run_polling()


if __name__ == '__main__':
    main()
