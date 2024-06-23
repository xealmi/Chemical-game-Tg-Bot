from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Awaitable, Dict, Any
from keyboards import builders
from data.subloader import get_json

class CheckSubscription(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ):
        count = 0
        sponsors = [f'@{i[20:]}' for i in await get_json('sponsors.json')]
        for i in sponsors:
            chat_member = await event.bot.get_chat_member(chat_id=i, user_id= event.from_user.id)
            if chat_member.status == 'left':
                count+=1
        
        if count !=0:
            await event.answer('Простите, но этот бот работает только благдаря спонсорам, поэтому, пожалуйста, подпишитесь на них', reply_markup= await builders.sponsors_kb_builder())
        else:
            return await handler(event, data)