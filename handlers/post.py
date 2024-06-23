from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.states import Post
from data.subloader import get_json
from keyboards import reply

router = Router()


@router.message(F.text.lower() == 'пост')
async def post(message:Message, state:FSMContext):
    data = await get_json('data.json')
    if data[str(message.from_user.id)]['status'] == 'Гл.Админ':
        await state.set_state(Post.message)
        await message.answer(text='Отправьте пост')

@router.message(Post.message)
async def send_post(message:Message, state:FSMContext):
    await state.clear()
    count = 0
    data = await get_json('data.json')
    for i in data.keys():
        await message.send_copy(chat_id=int(i))
        count+=1
    await message.answer(text=f'Пост был отправлен в {count} чатов', reply_markup=reply.menu_rkb)