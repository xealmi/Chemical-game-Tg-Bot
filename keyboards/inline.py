from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

first_chemical_element_kb= InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Открыть первый элемент', callback_data='открыть первый элемент')]
    ]
)

def cases_kb(cases):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'⚪Открыть обычный кейс ({cases['common_case']} шт.)', callback_data='open_c_case')],
            [InlineKeyboardButton(text=f'🟣Открыть эпический кейс ({cases['epic_case']} шт.)', callback_data='open_e_case')],
            [InlineKeyboardButton(text=f'🟡Открыть легендарный кейс ({cases['legendary_case']} шт.)', callback_data='open_l_case')],
            [InlineKeyboardButton(text=f'🔴Открыть мифичский кейс ({cases['mythical_case']} шт.)', callback_data='open_m_case')]
        ]
    )
    return kb

def laboratory_kb(eprice, name, iprice):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'Получить {name} ({eprice} кДж)', callback_data='buy_el')],
            [InlineKeyboardButton(text=f'Получить новый изотоп ({iprice} кДж)', callback_data='buy_is')]
        ]
    )
    return kb