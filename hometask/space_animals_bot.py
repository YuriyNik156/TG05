import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import requests
import random

from config import TOKEN5, API_NINJAS_KEY

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

# ANIMAL FACT
def get_random_animal_fact():
    url = "https://catfact.ninja/fact"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("fact", "Факт не найден.")
    return "Не удалось получить факт."

# GENERAL FACT (API Ninjas)
def get_random_general_fact():
    url = "https://api.api-ninjas.com/v1/facts"
    headers = {"X-Api-Key": API_NINJAS_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()[0].get("fact", "Факт не найден.")
    return "Не удалось получить факт."

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я научный бот 🤖\n"
        "Доступные команды:\n"
        "/spacex - Последний запуск SpaceX 🚀\n"
        "/animal_fact — Факт про животное 🐾\n"
        "/general_fact — Общий научный факт 🧠"
    )

@dp.message(Command("spacex"))
async def send_space_info(message: Message):
    launch = get_random_spacex_launch()
    if launch:
        text = f"🚀 Название запуска: {launch['name']}\n📅 Дата: {launch['date']}\n📝 {launch['details']}"
        await message.answer_photo(photo=launch['patch'], caption=text)
    else:
        await message.answer("Не удалось получить данные о запуске SpaceX.")

@dp.message(Command("animal_fact"))
async def send_animal_fact(message: Message):
    fact = get_random_animal_fact()
    await message.answer(f"🐾 Факт: {fact}")

@dp.message(Command("general_fact"))
async def send_general_fact(message: Message):
    fact = get_random_general_fact()
    await message.answer(f"🧠 Факт: {fact}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())