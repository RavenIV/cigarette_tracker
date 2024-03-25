from datetime import datetime

from aiogram import Dispatcher, F, types
from aiogram.filters import CommandStart

from config import API_HOST
from handlers.api import BotAPI
from handlers.utils import get_next_smoking_time, localize_time

dp = Dispatcher()
api = BotAPI(API_HOST)

START_MESSAGE = (
    'Привет, {}! 👋🏻\n\n'
    'Я помогу тебе бросить курить.\n'
    'Пиши мне о каждой выкуренной сигарете 🚬, а я рассчитаю время 🕘, '
    'когда ты сможешь покурить в следующий раз. '
    'Постепенно увеличивая интервалы между сигаретами, '
    'ты сможешь наконец-то бросить пагубную привычку 😎\n\n'
    'P.S. Имей в виду, я показываю <b>московское</b> время.'
)
SMOKED_CIGARETTE = '🚬 Сигарета'
WHEN_SMOKE = '🕘 Когда курить?'
LACK_OF_DATA = (
    'Недостаточно данных. '
    'Зафиксируй время хотя бы двух выкуренных сигарет 🚬 .'
)
RECOMMENDED_TIME = (
    'Последняя сигарета выкурена в {last_time}.\n\n'
    'Постарайся <i>не курить</i> до <b>{next_time}</b>.'
)


@dp.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    kb = [
        [
            types.KeyboardButton(text=SMOKED_CIGARETTE),
            types.KeyboardButton(text=WHEN_SMOKE)
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(
        START_MESSAGE.format(message.from_user.first_name),
        reply_markup=keyboard
    )


@dp.message(F.text == SMOKED_CIGARETTE)
async def fix_smoking_time(message: types.Message):
    smoking_time = message.date.isoformat()
    api.add_user_cigarette(message.from_user.id, smoking_time)
    await message.reply('Ок')


@dp.message(F.text == WHEN_SMOKE)
async def show_recommended_time(message: types.Message):
    cigars = api.get_last_cigarettes(message.from_user.id)
    if len(cigars) < 2:
        await message.reply(LACK_OF_DATA)
    else:
        last_time = datetime.fromisoformat(cigars[0]['smoking_time'])
        penultimate_time = datetime.fromisoformat(cigars[1]['smoking_time'])
        await message.reply(
            RECOMMENDED_TIME.format(
                last_time=localize_time(last_time),
                next_time=get_next_smoking_time(last_time, penultimate_time)
            )
        )
