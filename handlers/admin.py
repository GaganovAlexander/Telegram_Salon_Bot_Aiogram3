from os import getenv

from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher, F
from aiogram.filters import Command
from create_bot import bot

from sqlite_db import get_admins_id, add_admin, sql_add_command, sql_change_command, sql_delete_command, sql_pricelist_command
from commands import set_admin_commands
from handlers.client import pricelist_command


class FSM_Admin(StatesGroup):
    password_check = State()

    add_photo = State()
    add_name = State()
    add_description = State()
    add_price = State()

    delete_name = State()

    change_choice = State()
    change_select_item = State()
    change_new_value = State()



async def admin_command(message: Message, state: FSMContext):
    if message.from_user.id not in map(int, (await get_admins_id())[0]):
        await message.reply('Введите пороль админимстратора:')
        await state.set_state(FSM_Admin.password_check)
    else:
        await set_admin_commands(bot)
        await message.reply('Вы уже администратор')

async def password_handler(message: Message, state: FSMContext):
    if message.text == getenv('PASSWORD'):
        await add_admin(str(message.from_user.id))
        await set_admin_commands(bot)
        await message.reply('Успешно')      
    else:
        await message.reply('Ошибка или неверно введённый пароль')
    await state.clear()


async def add_command(message: Message, state: FSMContext):
    if message.from_user.id in map(int, (await get_admins_id())[0]):
        await state.set_state(FSM_Admin.add_photo)
        await message.reply('Загрузите фото')
    else:
        await message.reply('Вы не обладаете правами администратора')

async def add_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id)
    await state.set_state(FSM_Admin.add_name)
    await message.reply('Теперь введите название')

async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FSM_Admin.add_description)
    await message.reply('Теперь введите описание')   

async def add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(FSM_Admin.add_price)
    await message.reply('Теперь введите цену(через точку, в слуае цены с копейками, например: 499.99)')

async def add_price(message: Message, state: FSMContext):
    data = await state.get_data()
    if float(message.text) == float(message.text)//1:
        data['price'] = int(float(message.text))
    else:
        data['price'] = float(message.text)
    await sql_add_command(data)
    await message.reply('Готовый результат:')
    await message.answer_photo(data['photo'], caption=f"Имя: {data['name']}\nОписание: {data['description']}\nЦена: {data['price']}₽")
    await state.clear()


async def delete_command(message: Message, state: FSMContext):
    if message.from_user.id in map(int, (await get_admins_id())[0]):
        await pricelist_command(message)
        await message.reply('Введите название того, что хотите удалить')
        await state.set_state(FSM_Admin.delete_name)
    else:
        await message.reply('Вы не обладаете правами администратора')

async def delete_item(message: Message, state: FSMContext):
    await sql_delete_command(message.text)
    await message.reply('Готово')
    await state.clear()


async def change_command(message: Message, state: FSMContext):
    if message.from_user.id in map(int, (await get_admins_id())[0]):
        await pricelist_command(message)
        await message.reply('Введите название того, что хотите изменить')
        await state.set_state(FSM_Admin.change_choice)
    else:
        await message.reply('Вы не обладаете правами администратора')

async def change_choice(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.reply('Введите название поля, которое хотите изменить(photo, name, description или price)')
    await state.set_state(FSM_Admin.change_select_item)

async def change_select_item(message: Message, state: FSMContext):
    await state.update_data(item=message.text)
    await message.reply('Введите новое значение')
    await state.set_state(FSM_Admin.change_new_value)

async def change_new_value(message: Message, state: FSMContext):
    data = await state.get_data()
    await sql_change_command(data['name'], data['item'], message.text)
    await message.reply('Готово')
    await state.clear()


async def cancel_command(message: Message, state: FSMContext):
    if await state.get_state():
        await state.clear()
        await message.reply('OK')


def register_handlers_admin(dp: Dispatcher):
    dp.message.register(cancel_command, Command(commands='cancel'))

    dp.message.register(admin_command, Command(commands='admin'))
    dp.message.register(password_handler, FSM_Admin.password_check)

    dp.message.register(add_command, Command(commands='add'))
    dp.message.register(add_photo, FSM_Admin.add_photo, F.photo)
    dp.message.register(add_name, FSM_Admin.add_name)
    dp.message.register(add_description, FSM_Admin.add_description)
    dp.message.register(add_price, FSM_Admin.add_price)

    dp.message.register(delete_command, Command(commands='delete'))
    dp.message.register(delete_item, FSM_Admin.delete_name)

    dp.message.register(change_command, Command(commands='change'))
    dp.message.register(change_choice, FSM_Admin.change_choice)
    dp.message.register(change_select_item, FSM_Admin.change_select_item)
    dp.message.register(change_new_value, FSM_Admin.change_new_value)
