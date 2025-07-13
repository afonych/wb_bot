from bot.bot import dp, bot
from aiogram.utils import executor

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True) 