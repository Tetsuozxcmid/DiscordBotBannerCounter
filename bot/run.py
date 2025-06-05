import asyncio
from models.bot_model import Bot
from api.services.counter import main
import logging


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())