from lib.config import load_config
from lib.di import initialize

def main():
    config = load_config()
    bot = initialize(config)
    bot.start()

if __name__ == "__main__":
    main()
