from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

first_chemical_element_kb= InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Открыть новый элемент', callback_data='открыть первый элемент')]
    ]
)