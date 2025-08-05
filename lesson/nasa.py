import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import random
import requests
from datetime import datetime, timedelta

from config import TOKEN, NASA_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_random_apod():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    random_date = start_date + (end_date - start_date) * random.random()
    date_str = random_date.strftime("%Y-%m-%d")

    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}"
    print(f"[DEBUG] URL запроса: {url}")  # ← ВАЖНО!

    headers = {"User-Agent": "apod-bot/1.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 403:
        print("[ERROR] Доступ запрещён. Возможно, ключ неактивен или превышен лимит.")
        return {"title": "Ошибка 403: доступ запрещён", "url": "", "media_type": "error"}

    if response.status_code != 200:
        print(f"[ERROR] Статус: {response.status_code}")
        print(f"[ERROR] Ответ: {response.text}")
        return {"title": f"Ошибка {response.status_code}", "url": "", "media_type": "error"}

    try:
        return response.json()
    except Exception as e:
        print(f"[ERROR] JSON Decode: {e}")
        print(f"[ERROR] Ответ: {response.text}")
        return {"title": f"Ошибка парсинга JSON", "url": "", "media_type": "error"}

@dp.message(Command("random_apod"))
async def random_apod(message: Message):
    apod = get_random_apod()
    title = apod.get("title", "Без названия")
    media_type = apod.get("media_type")
    url = apod.get("url", "")

    if media_type == "image" and url:
        await message.answer_photo(photo=url, caption=title)
    else:
        await message.answer(f"{title}\n{url}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())