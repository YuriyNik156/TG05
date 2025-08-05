import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import requests
import random

from config import TOKEN5

bot = Bot(token=TOKEN5)
dp = Dispatcher()

# SPACE X API
def get_random_spacex_launch():
    url = "https://api.spacexdata.com/v5/launches"
    response = requests.get(url)
    if response.status_code == 200:
        launches = response.json()
        launch = random.choice(launches)
        return {
            "name": launch["name"],
            "details": launch.get("details", "Без описания"),
            "date": launch["date_utc"],
            "patch": launch["links"]["patch"]["small"]
        }
    return None

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я научный бот 🤖\n"
        "Доступные команды:\n"
        "/spacex - Последний запуск SpaceX 🚀\n"
    )

@dp.message(Command("spacex"))
async def send_space_info(message: Message):
    launch = get_random_spacex_launch()
    if launch:
        text = f"🚀 Название запуска: {launch['name']}\n📅 Дата: {launch['date']}\n📝 {launch['details']}"
        await message.answer_photo(photo=launch['patch'], caption=text)
    else:
        await message.answer("Не удалось получить данные о запуске SpaceX.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())