from dotenv import load_dotenv
load_dotenv()

import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from db.client import get_supabase



API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    supabase = get_supabase()
    telegram_id = message.from_user.id

    # Проверяем, есть ли пользователь в таблице
    user = supabase.table("wb_users").select("*").eq("telegram_id", telegram_id).execute()
    if not user.data:
        # Если нет — создаём
        supabase.table("wb_users").insert({"telegram_id": telegram_id}).execute()
        await message.reply("Вы зарегистрированы! Пожалуйста, отправьте свой API-ключ Wildberries для начала работы.")
    else:
        await message.reply("Вы уже зарегистрированы! Пожалуйста, отправьте свой API-ключ Wildberries для начала работы.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True) 