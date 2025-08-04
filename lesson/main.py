import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery

import random
from dotenv import load_dotenv
import os

from gtts import gTTS
import keyboards as kb

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('video'))
async def video(message:Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile("Стоковое видео.mp4")
    await bot.send_video(message.chat.id, video)

@dp.message(Command('voice'))
async def voice(message:Message):
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)

@dp.message(Command('doc'))
async def doc(message:Message):
    doc = FSInputFile("База данных бота.pdf")
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('audio'))
async def audio(message:Message):
    audio = FSInputFile("Стоковое аудио Show-Me-Again.m4a")
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('training'))
async def training(message:Message):
    training_list = [
        "Тренировка 1: Скакалка или имитация (прыжки на месте) – 2 мин., Берпи без отжимания – 3 подхода по 10–12 раз., Скручивания лёжа (пресс) – 3 подхода по 15–20 раз., Планка – 3 подхода по 30 сек (или сколько выдержишь)., Бег на месте с высоким подниманием колен – 2 мин.",
        "Тренировка 2: Приседания с собственным весом – 3×15., Отжимания (на коленях или классические) – 3×10–15., Ягодичный мост (лёжа, таз вверх) – 3×15., Супермен (лёжа на животе, руки и ноги вверх) – 3×12., Планка на боку – по 20–30 сек на каждую сторону.",
        "Тренировка 3: Прыжки в сторону (имитируем конькобежцев)., Отжимания + колено к груди., Приседания с выпрыгиванием., Альпинист (упор лёжа, колени к груди).",
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша тренировка на сегодня - {rand_tr}")

    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("training.ogg")
    audio = FSInputFile("training.ogg")
    await bot.send_voice(message.chat.id, audio)
    os.remove("training.ogg")

@dp.message(Command('photo', prefix='&'))
async def photo(message:Message):
    list = ['https://yandex-images.clstorage.net/96Uyv3j86/b63a54gIYK2/C3gDZho-5xkbvyZv6OybDp6ohhsvTtrsQsuB9SL6JAH_niWOtLHBaBdfOnUfXk_lkkenU9So8a1D6aMvJeeDch48EHfI-PIMynkzbegt24nJ-EJcOc_NqtJcljH0eSfA69CrBmisTvaPVSdr1Y2aptIHd1RRbWsj06vn97W_xHsCsU2n22yhXllooa5pLJsJjijKFLxHDmbFWF_0Yzw-1bEepA_kJwd3QZOopVZF02lQSz2Pk6zq4IKlrnB5swh4Cv-NZ5ogKBvaIGMiJqYeTYxqCV62B8Hoj5CYt6szvFV1GqxDZqkLNYacaitYS1vv3oI9itDsLqiDYu77uD8JN8G_we9UZmXRG60joyAlH8QHbQUb-QHPbwmVXrPif_AaPlMtjCCpQ_EHFiKilMVfJZFCcM3eamghAurmu324Sj6IPErqEO5oXJRt6utuYZnBRGgLHTRGB6hJ2tY4aXDz2TKW7Y9mZEV7x9wna9qK3uzeTX_F2eRp6Uii6Dg6NEfxAPuPIF-hLphb7mLrI-8eAsBoBhI6jcCqz9LfN-F49JL1H-aDIaSKuYXd4uoURxAm0UuxjpTkIqhFpyA-N_rLvs88iizfradaUmrsbWjmWYTAb0FV_QGNb8eZWH6vN_tdehuuxWalR3dAFSRr3kgX4ZvMew9Rai6iTmoj-P-0CP4Ff4EslGkmGN8m6GnqIJ8NzmDFHL5GDCzPWJX4brI-mPoRaoVh6Ad4CNbnL5QKl2gahLHNG26sIQ_qIXCyvkbxS35JZJit7B4RbC1lJ2caisSgxdf0BUTszdDev6F5fFTzn6LEYulEdcLSK6cSAh6s00e8xNSg5ylJIOY08rPAvsgzDuBa76zT3q7pIadk0YtLI8yYN4-HKEaSnLOrsDwaOpnpwmohgDhJm6VqH41coZdEdYzQZOXpSCXne7p7CTNP_YNskilvm15lIuNvI9IKwSmMV_COxC-DXZjwbo',
            'https://avatars.mds.yandex.net/i?id=3074a425cf41a9d08b667f11ec637593-5433422-images-thumbs&n=13',
            'https://avatars.mds.yandex.net/i?id=1d578c6bae85f9b4167292efeaf57f7cb097fad7-5263409-images-thumbs&n=13']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

@dp.message(F.photo)
async def react_photo(message:Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(F.text == "Что такое ИИ?")
async def aitext(message:Message):
    await message.answer('Искусственный интеллект (ИИ) — это комплекс технологических решений, который позволяет '
                         'машинам имитировать человеческое мышление, учиться на данных и принимать решения.')

@dp.callback_query(F.data == "news")
async def news(callback: CallbackQuery):
    await callback.answer("Новости подгружаются", show_alert=True)
    await callback.message.edit_text("Вот свежие новости!", reply_markup=await kb.test_keyboard())

@dp.message(F.text == "Тестовая кнопка 1")
async def test_button(message:Message):
    await message.answer('Обработка нажатия на reply кнопку')

@dp.message(Command('help'))
async def help(message:Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help')

@dp.message(CommandStart())
async def start(message:Message):
    await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=kb.inline_keyboard_test)

@dp.message()
async def start(message:Message):
    if message.text.lower() == "тест":
        await message.answer("тестируем")
    else:
        await message.send_copy(chat_id=message.chat.id)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
