from aiogram import Dispatcher, Bot
import asyncio
from config_reader import config
from aiogram.client.default import DefaultBotProperties
from handlers import user_commands, bot_messages, post
from middlewares.check_sub import CheckSubscription
from middlewares.antiflood import AntiFloodMiddleWare



async def main():
    bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='html'))
    dp = Dispatcher()
    
    dp.message.middleware(AntiFloodMiddleWare())
    dp.message.middleware(CheckSubscription())
    
    dp.include_routers(
        user_commands.router,
        post.router,
        bot_messages.router
    )
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    print('Бот запущен')
    asyncio.run(main())