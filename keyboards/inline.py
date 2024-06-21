from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from scripts import scripts

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

def shop_kb(qua_labs):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Купить кейс', callback_data='buy_case')],
            [InlineKeyboardButton(text=f'Купить лаборанта ({scripts.lab_price_calc(qua_labs)} кДж)', callback_data='buy_lab')]
        ]
    )
    return kb

def case_shop_kb():
    cases = scripts.case_price()
    cc = []
    max = 0
    for i in cases:
        i = str(i)
        if len(i)>max:
            max = len(i)
    for i in cases:
        i = str(i)
        if len(i)<max:
            i=i+('_'*(max-len(i)))
        cc.append(i)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'⚪Купить обычный кейс ({cases[0]} кДж)', callback_data=f'buy_common_case{cc[0]}')],
            [InlineKeyboardButton(text=f'🟣Купить эпический кейс ({cases[1]} кДж)', callback_data=f'buy_epic_case{cc[1]}')],
            [InlineKeyboardButton(text=f'🟡Купить легендарный кейс ({cases[2]} кДж)', callback_data=f'buy_legendary_case{cc[2]}')],
            [InlineKeyboardButton(text=f'🔴Купить мифичский кейс ({cases[3]} кДж)', callback_data=f'buy_mythical_case{cc[3]}')],
            [InlineKeyboardButton(text='<<Назад', callback_data='case_shop_back')]
        ])
    return kb