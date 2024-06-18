from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

rmk = ReplyKeyboardRemove()

menu_rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='👤Профиль')],
        [KeyboardButton(text='💡Собрать энергию')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)