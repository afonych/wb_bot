import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from .states import UserStates
from db.client import get_supabase
from .bot import dp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Загрузка внешних текстов
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_welcome():
    with open(os.path.join(BASE_DIR, 'texts', 'welcome.html'), encoding='utf-8') as f:
        return f.read()

def load_instruction():
    with open(os.path.join(BASE_DIR, 'texts', 'bot_instruction.txt'), encoding='utf-8') as f:
        return f.read()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    supabase = get_supabase()
    telegram_id = message.from_user.id
    user = supabase.table("wb_users").select("*").eq("telegram_id", telegram_id).execute()
    if not user.data:
        supabase.table("wb_users").insert({"telegram_id": telegram_id}).execute()
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Ввести API ключ WB", callback_data="enter_wb_key")
    )
    await message.answer(load_welcome(), reply_markup=kb, parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == "enter_wb_key")
async def on_enter_wb_key(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Пожалуйста, отправьте ваш WB API ключ.")
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

# Болталка через ИИ (заглушка)
@dp.message_handler(state=None)
async def ai_chat(message: types.Message, state: FSMContext):
    # Здесь будет интеграция с OpenAI, пока просто шаблонный ответ
    instruction = load_instruction()
    await message.reply(f"🤖 <i>Бот-ассистент:</i>\n{instruction}", parse_mode="HTML") 