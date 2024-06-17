from aiogram import F,Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

#======================================================================================

router = Router()

#======================================================================================

initial_photo = FSInputFile('data/images/StartImage.jpg')

#======================================================================================

@router.message(CommandStart())
async def start(message:Message):
    await message.answer_photo(
        photo=initial_photo,
        caption='⚗Приветствую, юный химик!'
    )