from aiogram import types
from aiogram.dispatcher import FSMContext
from .states import UserStates
from db.client import get_supabase
from .bot import dp

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    supabase = get_supabase()
    telegram_id = message.from_user.id

    user = supabase.table("wb_users").select("*").eq("telegram_id", telegram_id).execute()
    if not user.data:
        supabase.table("wb_users").insert({"telegram_id": telegram_id}).execute()
        await message.reply("Вы зарегистрированы! Пожалуйста, отправьте свой API-ключ Wildberries для начала работы.")
    else:
        await message.reply("Вы уже зарегистрированы! Пожалуйста, отправьте свой API-ключ Wildberries для начала работы.")
    await UserStates.waiting_for_wb_api_key.set()

@dp.message_handler(state=UserStates.waiting_for_wb_api_key)
async def process_wb_api_key(message: types.Message, state: FSMContext):
    wb_api_key = message.text.strip()
    if len(wb_api_key) < 32:
        await message.reply("Похоже, это невалидный ключ. Пожалуйста, отправьте корректный WB API ключ.")
        return
    parts = wb_api_key.split('.')
    if len(parts) != 3 or any(len(p) == 0 for p in parts):
        await message.reply("Похоже, это невалидный ключ. Пожалуйста, отправьте корректный WB API ключ.")
        return
    supabase = get_supabase()
    telegram_id = message.from_user.id
    supabase.table("wb_users").update({"wb_api_key": wb_api_key}).eq("telegram_id", telegram_id).execute()
    await message.reply("Ваш WB API ключ сохранён! Теперь вы можете пользоваться ботом.")
    await state.finish() 