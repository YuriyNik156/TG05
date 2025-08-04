import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

from config import TOKEN2
from deep_translator import GoogleTranslator
import os

from gtts import gTTS

bot = Bot(token=TOKEN2)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message:Message):
    await message.answer(f"Привет, {message.from_user.first_name}")

@dp.message(Command("help"))
async def help(message:Message):
    await message.answer("Данный бот умеет выполнять команды: \n /start \n /help")

#Отправьте с помощью бота голосовое сообщение
@dp.message(Command("voice"))
async def send_voice(message:Message):
    text = "Привет! Это голосовое сообщение от бота!"
    tts = gTTS(text=text, lang="ru")
    tts.save("voice.ogg")

    voice = FSInputFile("voice.ogg")
    await bot.send_voice(message.chat.id, voice)
    os.remove("voice.ogg")

# Напишите код для сохранения всех фото, которые отправляет пользователь боту в папке img
@dp.message(F.photo)
async def save_photo(message:Message):
    os.makedirs("../img", exist_ok=True) # Создаем папку img
    await bot.download(message.photo[-1], destination=f"img/{message.photo[-1].file_id}.jpg")
    await message.answer("Фото сохранено в папке img")

#Напишите код для перевода любого текста, который пишет пользователь боту, на английский язык
@dp.message(F.text)
async def translate_to_english(message:Message):
    translated_text = GoogleTranslator(source="auto", target="en").translate(message.text)
    await message.answer(f"Перевод на английский: \n {translated_text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
