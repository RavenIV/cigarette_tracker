import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.enums import ParseMode

from config import TOKEN

from handlers.actions import dp


if not TOKEN:
    raise UnboundLocalError('Отсутствует TELEGRAM_TOKEN.')

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
