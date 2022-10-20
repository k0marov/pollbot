import asyncio
import os

from di import initialize_bot

TOKEN_KEY = "ANONYMOUS_POLL_BOT_TOKEN"

def main():
    token = os.environ.get(TOKEN_KEY)
    if token is None:
        print("Please fill in the "+ TOKEN_KEY + " env variable.")
        return
    bot = initialize_bot(token)
    bot.start()


if __name__ == "__main__":
    main()
