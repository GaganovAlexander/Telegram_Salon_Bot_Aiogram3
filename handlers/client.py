from os import getenv

from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.filters import Command

from sqlite_db import sql_pricelist_command
from commands import set_client_commands
from create_bot import bot


async def start_command(message: Message):
    await message.answer(f'{message.from_user.full_name}, здравствуйте!')
    await set_client_commands(bot)

async def address_command(message: Message):
    await message.answer(getenv('ADDRESS'))

async def pricelist_command(message: Message):
    for i in await sql_pricelist_command():
        await message.answer_photo(i[0], caption=f'Название: {i[1]}\nОписание: {i[2]}\nЦена: {i[3]}₽')

async def get_contacts_command(message: Message):
    await message.answer(getenv('CONTACTS'))


def register_handlers_client(dp: Dispatcher):
    dp.message.register(start_command, Command(commands='start'))
    dp.message.register(address_command, Command(commands='address'))
    dp.message.register(pricelist_command, Command(commands='pricelist'))
    dp.message.register(get_contacts_command, Command(commands='get_contacts'))