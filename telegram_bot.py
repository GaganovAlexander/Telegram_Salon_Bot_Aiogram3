from asyncio import run as arun

from create_bot import bot, dp
from handlers import register_handlers_client, register_handlers_admin
from sqlite_db import sql_start


async def start():
    #await bot.send_message(1189892244, 'Запустилось')
    print('Бот запущен')
    await sql_start()
    await bot.delete_webhook(drop_pending_updates=True)
    
async def main():
    dp.startup.register(start)

    register_handlers_client(dp)
    register_handlers_admin(dp)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    arun(main())