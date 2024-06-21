from aiogram import F, Router
from aiogram.types import Message, FSInputFile, CallbackQuery
from data.subloader import get_json, load_json
from keyboards import reply, inline
from datetime import datetime, timedelta
from scripts.scripts import case_roll, is_price_calc, ch_el_price_calc, lab_price_calc, income_calc

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
        prem = (datetime.fromisoformat(user_data['premium']) - datetime.today()).days>0
        await message.answer_photo(
            photo=profile_photo,
            caption=
            f'👤{message.from_user.full_name}\n'
            '-----------\n'
            f'⚛Последний открытый элемент: <b>{(await get_json('chemical_elements.json'))[str(user_data['chemical_element'])]['symbol']}</b>\n'
            f'🌟Открыто элементов: <b>{user_data['chemical_element']}</b>\n'
            f'💥Баланс: <b>{user_data['balance']} кДж</b>\n'
            f'Энерговыработка: <b>{income_calc(user_data['chemical_element'], user_data['isotopes'], user_data['labs']) * (2 if prem else 1)} кДж/мин</b>\n'
            '-----------\n'
            f'💳Premium: {f'до {user_data['premium'][:-7]}' if prem else 'Отсутствует'}',
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
        prem = (datetime.fromisoformat(user_data['premium']) - now).days>0
        if time !=0:
            if prem:
                if time>480:
                    time =480
            else:
                if time>240:
                    time =240
            income = income_calc(user_data['chemical_element'], user_data['isotopes'], user_data['labs']) * time * (2 if prem else 1)
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
        await message.answer(text=f'Ваши кейсы:', reply_markup=inline.cases_kb(user_data['cases']))
    else:
        await message.answer(text='Для начала откройте хотя бы один химический элемент')



@router.callback_query(F.data.casefold().in_(['open_c_case','open_e_case','open_l_case','open_m_case']))
async def open_case(callback: CallbackQuery):
    data = await get_json('data.json')
    user_data = data[str(callback.from_user.id)]
    lvl = user_data['chemical_element']
    
    if callback.data == 'open_c_case':
        selected_case = 'common_case'
    elif callback.data == 'open_e_case':
        if lvl <3:
            selected_case = 0
            await callback.answer(text='Этот кейс доступен с 3 химического элемента')
        else:
            selected_case = 'epic_case'
    elif callback.data == 'open_l_case':
        if lvl <6:
            selected_case = 0
            await callback.answer(text='Этот кейс доступен с 6 химического элемента')
        else:
            selected_case = 'legendary_case'
    else:
        if lvl <9:
            selected_case = 0
            await callback.answer(text='Этот кейс доступен с 9 химического элемента')
        else:
            selected_case = 'mythical_case'
    
    if selected_case !=0:
        if user_data['cases'][selected_case] == 0:
            await callback.answer(text='У вас нет кейсов такого типа!')
        else:
            res = case_roll(selected_case)
            user_data['cases'][selected_case]-=1
            if isinstance(res, int):
                user_data['balance'] += res
                await callback.message.answer(text=f'Поздравляем! Вы выиграли <b>{res} кДж</b>!')
            
            elif res == 'add_is':
                user_data['isotopes'] +=1
                await callback.message.answer(text=f'Поздравляем! Вы выиграли <b>открытие нового изотопа</b>!')
            
            elif res == 'add_el':
                user_data['chemical_element']+=1
                await callback.message.answer(text=f'Поздравляем! Вы выиграли <b>открытие нового химического элемента</b>!')
            
            elif res== 'prem3d':
                today =datetime.today()
                if (datetime.fromisoformat(user_data['premium']) - today).days>0:
                    user_data['premium'] = str(datetime.fromisoformat(user_data['premium']) + timedelta(days=3))
                else:
                    user_data['premium'] = str(today + timedelta(days=3))
                await callback.message.answer(text=f'Поздравляем! Вы выиграли <b>премиум на 3 дня</b>!🤯')
            
            else:
                user_data['cases'][res] +=1
                if res =='common_case':
                    res = 'обычный' 
                elif res =='epic_case':
                    res = 'эпический' 
                elif res =='legendary_case':
                    res = 'легендарный' 
                else:
                    res = 'мифический' 
                await callback.message.answer(text=f'Поздравляем! Вы выиграли <b>{res} кейс</b>!')
            
            await callback.message.edit_reply_markup(reply_markup=inline.cases_kb(user_data['cases']))
            data[str(callback.from_user.id)] = user_data
            load_json('data.json', data)



@router.message(F.text.casefold().in_(['🧪лаборатория', 'лаборатория']))
async def laboratory(message:Message):
    data= await get_json('data.json')
    if str(message.from_user.id) in data:
        user_data = data[str(message.from_user.id)]
        x = user_data['chemical_element']+1
        chem_el = (await get_json('chemical_elements.json'))[str(x)]
        await message.answer(text='Выберите действие:', reply_markup=inline.laboratory_kb(round(10*3.2**x), chem_el['name'], round(10*(1.63)**(user_data['isotopes']+1))))
    else:
        await message.answer(text='Для начала откройте хотя бы один химический элемент')


# Следующая функция это самый чистый код в вашей жизни
@router.callback_query(F.data.casefold().in_(['buy_el', 'buy_is']))
async def laboratoey_buy(callback:CallbackQuery):
    if callback.data == 'buy_el':
        data = await get_json('data.json')
        user_data= data[str(callback.from_user.id)]
        # Проверка, будет ли баланс после вычитания стоимости отрицательным
        x =user_data['chemical_element']+1
        balance = user_data['balance']
        cost = ch_el_price_calc(x)
        new_balance = balance-cost
        
        if new_balance >=0:
            user_data['balance'] =new_balance
            chem_els = await get_json('chemical_elements.json')
            # Обновление хим. элиента в data.json
            user_data['chemical_element'] =x
            load_json('data.json', data)
            
            await callback.message.edit_reply_markup(
                reply_markup=inline.laboratory_kb(
                    ch_el_price_calc(x+1),
                    chem_els[str(x+1)]['name'],
                    is_price_calc(user_data['isotopes']+1)
                    )
                )
            await callback.message.answer(text=f'Поздравляем! Вы получили {chem_els[str(user_data['chemical_element'])]['name']}!')
        else:
            await callback.answer(text='😭Вам не хватает энергии!')
    
    elif callback.data == 'buy_is':
        data = await get_json('data.json')
        
        user_data =data[str(callback.from_user.id)]
        x =user_data['isotopes']+1
        balance = user_data['balance']
        
        if balance>=is_price_calc(x):
            chem_els = await get_json('chemical_elements.json')
            if x<=chem_els[str(user_data['chemical_element'])]['isotopes']:
                
                # Обновление изотопа в data.json
                user_data['balance'] =balance-is_price_calc(x)
                user_data['isotopes'] =x
                data[str(callback.from_user.id)] = user_data = user_data
                load_json('data.json', data)
                
                await callback.message.edit_reply_markup(
                    reply_markup=inline.laboratory_kb(
                        ch_el_price_calc(user_data['chemical_element']+1),
                        chem_els[str(user_data['chemical_element']+1)]['name'],
                        is_price_calc(x+1)
                        )
                    )
                await callback.message.answer(text=f'Поздравляем! Вы получили новый изотоп!')
            else:
                await callback.answer(text='Для этого откройте новый элемент!')
        else:
            await callback.answer(text='😭Вам не хватает энергии!')




@router.message(F.text.casefold().in_(['🏪магазин', 'магазин']))
async def shop(message:Message):
    data= await get_json('data.json')
    if str(message.from_user.id) in data:
        qua_lab= data[str(message.from_user.id)]['labs']
        await message.answer(text='Что Вы хотите приобрести?', reply_markup=inline.shop_kb(qua_lab))
    else:
        await message.answer(text='Для начала откройте хотя бы один химический элемент')

@router.callback_query(F.data.casefold().in_(['buy_case', 'buy_lab']))
async def shop_logic(callback: CallbackQuery):
    
    if callback.data == 'buy_case':
        await callback.message.edit_text(text='Какой кейс Вы хотите приобрести?', reply_markup=inline.case_shop_kb())
    
    elif callback.data == 'buy_lab':
        data = await get_json('data.json')
        user_data = data[str(callback.from_user.id)]
        
        ch_el = user_data['chemical_element']
        labs = user_data['labs']
        if ch_el>3:
            if labs+1 <=ch_el:
                cost = lab_price_calc(labs)
                if user_data['balance']<cost:
                    await callback.answer(text='😭Вам не хватает энергии!')
                else:
                    user_data['balance']-=cost
                    user_data['labs']+=1
                    await callback.message.edit_reply_markup(reply_markup=inline.shop_kb(labs+1))
                    await callback.message.answer(text='Поздравляем, Вы наняли лаборанта! Ваш доход увеличен на 10%')
                    data[str(callback.from_user.id)] = user_data
                    load_json('data.json', data)
            else:
                await callback.answer(text='Для этого откройте новый элемент!')
        else:
            await callback.answer(text='Для этого откройте Бериллий!')

@router.callback_query(F.data[:-5].casefold().in_(['buy_common_case','buy_epic_case','buy_legendary_case','buy_mythical_case']))
async def buy_case(callback:CallbackQuery):
    case = callback.data[4:][:-5]
    
    data = await get_json('data.json')
    user_data = data[str(callback.from_user.id)]
    price = callback.data[-5:]
    price = int(price.replace('_', ''))
    if user_data['balance']>=price:
        user_data['balance']-=price
        user_data['cases'][case]+=1
        data[str(callback.from_user.id)] = user_data
        await callback.answer(text='🎁Кейс успешно куплен')
        load_json('data.json', data)
    else:
        await callback.answer(text='😭Вам не хватает энергии!')