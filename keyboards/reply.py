from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

rmk = ReplyKeyboardRemove()

menu_rkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='👤Профиль')
            ],
        [
            KeyboardButton(text='💡Собрать энергию'),
            KeyboardButton(text='🧪Лаборатория')
        ],
        [KeyboardButton(text='🏪Магазин'),
        KeyboardButton(text='🎁Кейсы')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)