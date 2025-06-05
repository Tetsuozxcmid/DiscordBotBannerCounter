from models.bot_model import Bot
import asyncio

async def main():
    bot = Bot()
    await bot.start(bot.bot_token)