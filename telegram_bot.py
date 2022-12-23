import asyncio

from create_bot import bot, dp
from handlers import register_handlers_client
from sqlite_db.sqlite_db import sql_start

async def start():
    #await bot.send_message(1189892244, 'Запустилось')
    print('Бот запущен')
    sql_start()

    
async def main():
    dp.startup.register(start)

    register_handlers_client(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())