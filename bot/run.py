from models.bot_model import Bot
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot()
    bot.run(bot.bot_token)

if __name__ == "__main__":
    
    main()