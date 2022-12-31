from os import getenv

from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Dispatcher
from aiogram.filters import Command

from sqlite_db import sql_pricelist_command, get_num
from commands import set_client_commands
from keys import client_items_inlines
from filters import ClientInline
from create_bot import bot


class FSM_client(StatesGroup):
    book1 = State()



async def start_command(message: Message) -> None:
    """/Start command handler. Answer hello and turns on client's commands list"""
    await message.answer(f'{message.from_user.full_name}, здравствуйте!')
    await set_client_commands(bot)

async def address_command(message: Message) -> None:
    """/address command hadler. Answer address of the company"""
    await message.answer(getenv('ADDRESS'))

async def pricelist_command(message: Message) -> None:
    """/pricelist command handler. Answer multiple messages with pricelist rows(main photo, name, description and price), also \
        activate client pricelist inlines with 'more photos' and 'book' fucntional"""
    for i in await sql_pricelist_command():
        await message.answer_photo(FSInputFile(f'photos/{i[0]}/0.jpg'), caption=f'Название: {i[0]}\nОписание: {i[1]}\nЦена: {i[2]}₽', reply_markup=client_items_inlines(i[0]))

async def client_inlines(call: CallbackQuery, state: FSMContext) -> None:
    """More photos and book inlines keys handler"""
    data = call.data.split('_')
    match data[0]:
        case 'book':
            ...
            # state.set_state(FSM_client.book1)
        case 'photos':
            media = []
            num = (await get_num(data[1]))[0][0]
            for i in range(num):
                media.append(InputMediaPhoto(media=FSInputFile(f'photos/{data[1]}/{i}.jpg')))
            await call.message.answer_media_group(media)
    await call.answer()

async def get_contacts_command(message: Message) -> None:
    """Answer companies contacts"""
    await message.answer(getenv('CONTACTS'))


def register_handlers_client(dp: Dispatcher) -> None:
    """Register all clients handlers(both commands and inlines)"""
    dp.message.register(start_command, Command(commands='start'))
    dp.message.register(address_command, Command(commands='address'))
    dp.message.register(pricelist_command, Command(commands='pricelist'))
    dp.callback_query.register(client_inlines, ClientInline())
    dp.message.register(get_contacts_command, Command(commands='get_contacts'))