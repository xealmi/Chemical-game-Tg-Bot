from aiogram import F, Router
from aiogram.types import Message, FSInputFile, CallbackQuery
from data.subloader import get_json, load_json
from keyboards import reply, inline
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
            el_income = user_data['chemical_element']
            is_income = user_data['isotopes']
            income = (round((1-1.4**el_income)/(-0.4)) + round((1-1.05**is_income)/(-0.05)))*time
            user_data['balance'] += income
            user_data['last_profit_collection'] = str(now)
            await message.answer(text=f'💥Вы получили <b>{income} кДж</b> энергии')
            data[str(message.from_user.id)] = user_data
            load_json('data.json', data)
        else:
            await message.answer(text='Энергия ещё не выделилась!')
    else:
        await message.answer(text='Для начала откройте хотя бы один химический элемент')



@router.message(F.text.casefold().in_(['🎁кейсы', 'кейсы']))
async def cases(message:Message):
    data = await get_json('data.json')
    
    if str(message.from_user.id) in data:
        user_data = data[str(message.from_user.id)]
        cases = user_data['cases']
        await message.answer(text=f'Ваши кейсы:', reply_markup=inline.cases_kb(cases["common_case"], cases["epic_case"],cases["legendary_case"],cases["mythical_case"]))
    else:
        await message.answer(text='Для начала откройте хотя бы один химический элемент')



# @router.callback_query(F.data.casefold().in_(['open_c_case','open_e_case','open_l_case','open_m_case']))
# async def open_case(callback: CallbackQuery):
#     data = await get_json('data.json')
#     user_data = data[str(callback.from_user.id)]
#     lvl = user_data['chemical_element']
    
#     if callback.data == 'open_c_case':
#         selected_case = 'common_case'
#     elif callback.data == 'open_e_case':
#         if lvl <3:
#             selected_case = 0
#             await callback.answer(text='Этот кейс доступен с 3 химического элемента')
#         else:
#             selected_case = 'epic_case'
#     elif callback.data == 'open_l_case':
#         if lvl <6:
#             selected_case = 0
#             await callback.answer(text='Этот кейс доступен с 6 химического элемента')
#         else:
#             selected_case = 'legendary_case'
#     else:
#         if lvl <9:
#             selected_case = 0
#             await callback.answer(text='Этот кейс доступен с 9 химического элемента')
#         else:
#             selected_case = 'mythical_case'
    
#     if selected_case !=0:
#         if user_data['cases'][selected_case] == 0:
#             await callback.answer(text='У вас нет кейсов такого типа!')
#         else:



@router.message(F.text.casefold().in_(['🧪лаборатория', 'лаборатория']))
async def laboratory(message:Message):
    data= await get_json('data.json')
    if str(message.from_user.id) in data:
        user_data = data[str(message.from_user.id)]
        x = user_data['chemical_element']+1
        chem_el = (await get_json('chemical_elements.json'))[str(x)]
        await message.answer(text='Выберите действие:', reply_markup=inline.laboratory_kb(round(10*(2.8)**x), chem_el['name'], round(10*(1.63)**(user_data['isotopes']+1))))
    else:
        await message.answer(text='Для начала откройте хотя бы один химический элемент')


# Следующая функция самый чистый код в вашей жизни
@router.callback_query(F.data.casefold().in_(['buy_el', 'buy_is']))
async def laboratoey_buy(callback:CallbackQuery):
    if callback.data == 'buy_el':
        data = await get_json('data.json')
        
        # Проверка, будет ли баланс после вычитания стоимости отрицательным
        x =data[str(callback.from_user.id)]['chemical_element']+1
        balance = data[str(callback.from_user.id)]['balance']
        cost = round(10*(2.8)**x)
        new_balance = balance-cost
        
        if new_balance >=0:
            data[str(callback.from_user.id)]['balance'] =new_balance
            chem_els = await get_json('chemical_elements.json')
            # Обновление хим. элиента в data.json
            data[str(callback.from_user.id)]['chemical_element'] =x
            load_json('data.json', data)
            
            await callback.message.edit_reply_markup(
                reply_markup=inline.laboratory_kb(
                    round(10*(2.8)**(x+1)),
                    chem_els[str(x+1)]['name'],
                    round(10*(1.63)**(user_data['isotopes']+1))
                    )
                )
            await callback.message.answer(text=f'Поздравляем! Вы получили {chem_els[str(data[str(callback.from_user.id)]['chemical_element'])]['name']}!')
        else:
            await callback.answer(text='😭Вам не хватает энергии!')
    
    elif callback.data == 'buy_is':
        data = await get_json('data.json')
        
        # Проверка, будет ли баланс после вычитания стоимости отрицательным
        user_data =data[str(callback.from_user.id)]
        x =user_data['isotopes']+1
        balance = user_data['balance']
        cost = round(10*(1.63)**x)
        new_balance = balance-cost
        
        if new_balance >=0:
            chem_els = await get_json('chemical_elements.json')
            if x<=chem_els[str(user_data['chemical_element'])]['isotopes']:
                user_data['balance'] =new_balance
                # Обновление изотопа в data.json
                user_data['isotopes'] =x
                data[str(callback.from_user.id)] = user_data = user_data
                load_json('data.json', data)
                
                await callback.message.edit_reply_markup(
                    reply_markup=inline.laboratory_kb(
                        round(10*(2.8)**(user_data['chemical_element']+1)),
                        chem_els[str(user_data['chemical_element']+1)]['name'],
                        round(10*(1.63)**(x+1))
                        )
                    )
                await callback.message.answer(text=f'Поздравляем! Вы получили новый изотоп!')
            else:
                await callback.answer(text='Чтобы купить этот изотоп, откройте новый элемент!')
        else:
            await callback.answer(text='😭Вам не хватает энергии!')