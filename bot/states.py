from aiogram.dispatcher.filters.state import State, StatesGroup

class UserStates(StatesGroup):
    waiting_for_wb_api_key = State() 