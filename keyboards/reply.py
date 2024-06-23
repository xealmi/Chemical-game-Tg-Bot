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
        [
            KeyboardButton(text='🏪Магазин'),
            KeyboardButton(text='🎁Кейсы')
        ],
        [
            KeyboardButton(text='💰Донат'),
            KeyboardButton(text='🏅Топ')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)

send_or_no_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Да'),
       KeyboardButton(text='Нет')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)