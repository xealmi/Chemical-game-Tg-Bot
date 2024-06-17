from aiogram import F,Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery
from data.subloader import get_json, load_json
from keyboards import inline
from datetime import datetime

#======================================================================================

router = Router()

#======================================================================================

initial_photo = FSInputFile('data/images/StartImage.jpg')

#======================================================================================


@router.message(CommandStart())
async def start(message:Message):
    data = await get_json('data.json')
    value = str(message.from_user.id) in data
    await message.answer_photo(
        photo=initial_photo,
        caption='⚗Приветствую, юный химик!'
        '\n\nТебе предстоит открыть всевозможные химические элементы!'
        '\n\n<b>Удачи!</b>',
        reply_markup=None if value else inline.first_chemical_element_kb
    )

@router.callback_query(F.data == 'открыть первый элемент')
async def ivent_first_chemical_element(callback:CallbackQuery):
    data = await get_json('data.json')
    user_data = {
        'chemical_element': 1,
        'date_of_register': datetime.now().strftime('%d-%m-%y')
    }
    data[str(callback.from_user.id)] = user_data
    load_json('data.json', data)
    await callback.message.answer(text='Поздравляем! Вы получили свой первый химический элемент - водород')