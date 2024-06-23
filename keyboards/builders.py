from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.subloader import get_json

async def donate_kb_builder():
    data = await get_json('donate.json')
    
    builder = InlineKeyboardBuilder()
    [builder.button(text=f'{data[i]['title']} ({data[i]['price']}₽)', url=data[i]['url']) for i in data]
    builder.adjust(*[1])
    return builder.as_markup()

async def sponsors_kb_builder():
    data = await get_json('sponsors.json')
    
    builder = InlineKeyboardBuilder()
    [builder.button(text=data[i]['title'], url=data[i]['url']) for i in data]
    builder.adjust(*[1])
    return builder.as_markup()