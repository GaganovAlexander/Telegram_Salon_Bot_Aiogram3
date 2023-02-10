from os import getenv

from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.types.input_file import FSInputFile
from aiogram import Dispatcher
from aiogram.filters import Command

from sqlite_db import get_num, get_all_names, get_item
from commands import set_client_commands
from keys import client_items_inlines, client_pricelist_inlines
from filters import ClientInline
from create_bot import bot


async def start_command(message: Message) -> None:
    """/Start command handler. Answer hello and turns on client's commands list"""
    await message.answer(f'{message.from_user.first_name.capitalize()} {message.from_user.last_name.capitalize()}, здравствуйте!')
    await set_client_commands(bot)

async def pricelist_command(message: Message) -> None:
    names = list(map(lambda x: x[0], await get_all_names()))
    if len(names) > 6:
        last_num = 6
        first_page = True
    else:
        last_num = len(names) % 6
        first_page = False
    await message.answer('Прайс-лист:', reply_markup=client_pricelist_inlines(names[:last_num], last_num, first_page)) 

async def client_inlines(call: CallbackQuery) -> None:
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
            await call.message.answer(f'Больше фото по пунтку "{data[1]}":')
            await call.message.answer_media_group(media)
        case 'pricelist':
            match data[1]:
                case 'nextpage':
                    names = list(map(lambda x: x[0], await get_all_names()))
                    last_item_num = int(data[2])
                    if last_item_num + 6 < len(names):
                        last_num = last_item_num + 6
                        last_page = False
                    else:
                        last_num = last_item_num + len(names) % 6
                        last_page = True
                    await call.message.edit_reply_markup(reply_markup=client_pricelist_inlines(names[last_item_num:last_num],\
                        last_num, last_page=last_page))
                case 'prevpage':
                    names = list(map(lambda x: x[0], await get_all_names()))
                    last_item_num = int(data[2])
                    first_page = last_item_num // 6 == 1
                    await call.message.edit_reply_markup(reply_markup=client_pricelist_inlines(names[6*(last_item_num//6 - 1):last_item_num//6 * 6],\
                        last_item_num//6 * 6, first_page))
                case 'choice':
                    item = (await get_item(data[2]))[0]
                    await call.message.answer_photo(FSInputFile(f'photos/{item[0]}/0.jpg'),\
                        caption=f'Название: {item[0]}\nОписание: {item[1]}\nЦена: {item[2]}', reply_markup=client_items_inlines(item[0]))
    await call.answer()


def register_handlers_client(dp: Dispatcher) -> None:
    """Register all clients handlers(both commands and inlines)"""
    dp.message.register(start_command, Command(commands='start'))
    dp.message.register(pricelist_command, Command(commands='pricelist'))
    dp.callback_query.register(client_inlines, ClientInline())