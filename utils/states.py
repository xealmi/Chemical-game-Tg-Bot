from aiogram.fsm.state import StatesGroup, State

class Post(StatesGroup):
    message = State()