from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from data.subloader import get_json, load_json
from keyboards import reply
from datetime import datetime

#=======================================================================================

router = Router()

#=======================================================================================

profile_photo = FSInputFile('data/images/profile.jpg')

#=======================================================================================

@router.message(F.text.casefold().in_(['👤профиль', 'профиль']))
async def profile(message: Message):
    data = await get_json('data.json')
    if str(message.from_user.id) in data:
        user_data = data[str(message.from_user.id)]
        await message.answer_photo(
            photo=profile_photo,
            caption=f'👤{message.from_user.full_name}\n'
            '-----------\n'
            f'⚛Последний открытый элемент: <b>{(await get_json('chemical_elements.json'))[str(user_data['chemical_element'])]['symbol']}</b>\n'
            f'🌟Открыто элементов: <b>{user_data['chemical_element']}</b>\n'
            f'💥Баланс: <b>{user_data['balance']} кДж</b>',
            reply_markup=reply.menu_rkb
        )
    else:
        await message.answer(text='Для начала откройте хотя бы один химический элемент')


@router.message(F.text.casefold().in_(['💡собрать энергию', 'энергия', 'собрать энергию']))
async def collect_profit(message:Message):
    data = await get_json('data.json')
    
    if str(message.from_user.id) in data:
        user_data = data[str(message.from_user.id)]
        now = datetime.today()
        time = (now - datetime.fromisoformat(user_data['last_profit_collection'])).seconds//60
        if time !=0:
            income = user_data['income_per_minute']*time
            user_data['balance'] += income
            user_data['last_profit_collection'] = str(now)
            await message.answer(text=f'💥Вы получили <b>{income} кДж</b> энергии')
            data[str(message.from_user.id)] = user_data
            load_json('data.json', data)
        else:
            await message.answer(text='Вы ещё не выделили энергию!')
    else:
        await message.answer(text='Для начала откройте хотя бы один химический элемент')

