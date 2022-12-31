from os import getenv, mkdir, rename, remove

from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher, F
from aiogram.filters import Command
from create_bot import bot

from sqlite_db import get_admins_id, add_admin, sql_add_command, sql_change_command,\
    sql_delete_command, sql_pricelist_command, increase_num, get_num
from keys import admin_items_inlines, admin_photo_inlines
from commands import set_admin_commands
from filters import AdminFilter


# Admin's states group
class FSM_Admin(StatesGroup):
    password_check = State()

    add_photo = State()
    add_name = State()
    add_description = State()
    add_price = State()

    change_complite_text = State()
    change_complite_photo = State()

    add_more_photos = State()


async def admin_command(message: Message, state: FSMContext):
    """/admin command handler. If user already in admins list - do nothing, else answer him to enter password"""
    if message.from_user.id not in map(int, (await get_admins_id())[0]):
        await message.reply('Введите пороль админимстратора:')
        await state.set_state(FSM_Admin.password_check)
    else:
        await set_admin_commands(bot)
        await message.reply('Вы уже администратор')

async def password_handler(message: Message, state: FSMContext):
    """Admin password handler(after /admin command)"""
    if message.text == getenv('PASSWORD'):
        await add_admin(str(message.from_user.id))
        await set_admin_commands(bot)
        await message.reply('Успешно')      
    else:
        await message.reply('Ошибка или неверно введённый пароль')
    await state.clear()


async def admin_inlines(call: CallbackQuery, state: FSMContext):
    """All admin's inlines handler"""
    data = call.data.split('_')
    match data[0]:
        case 'delete':
            await sql_delete_command(data[1])
            await call.message.answer('Готово')
        case 'change':
            match data[1]:
                case 'photo':
                    media = []
                    num = (await get_num(data[2]))[0][0]
                    for i in range(num):
                        media.append(InputMediaPhoto(media=FSInputFile(f'photos/{data[2]}/{i}.jpg')))
                    await call.message.answer_media_group(media)
                    await call.message.answer('Выберите фото из списка или загрузите новое', reply_markup=admin_photo_inlines(num, data[2]))
                case 'name':
                    await state.set_state(FSM_Admin.change_complite_text)
                    await state.update_data(name=data[2], item='name')
                    await call.message.answer('Введите новое название')
                case 'description':
                    await state.set_state(FSM_Admin.change_complite_text)
                    await state.update_data(name=data[2], item='description')
                    await call.message.answer('Введите новое описание')
                case 'price':
                    await state.set_state(FSM_Admin.change_complite_text)
                    await state.update_data(name=data[2], item='price')
                    await call.message.answer('Введите новую цену')
        case 'add':
            await state.set_state(FSM_Admin.add_more_photos)
            await state.update_data(name=data[1])
            await call.message.answer('Отправьте фотографию')
        case 'mainphoto':
            rename(f"photos/{data[2]}/0.jpg", f"photos/{data[2]}/temp.jpg")
            rename(f"photos/{data[2]}/{data[1]}.jpg", f"photos/{data[2]}/0.jpg")
            rename(f"photos/{data[2]}/temp.jpg", f"photos/{data[2]}/{data[1]}.jpg")
            await call.message.answer('Готово')
        case 'new':
            await state.set_state(FSM_Admin.change_complite_photo)
            await state.update_data(name=data[1])
            await call.message.answer('Отправьте новое фото')
        case 'deletephoto':
            media = []
            num = (await get_num(data[1]))[0][0]
            for i in range(1, num):
                media.append(InputMediaPhoto(media=FSInputFile(f'photos/{data[1]}/{i}.jpg')))
            await call.message.answer_media_group(media)
            await call.message.answer('Выберите фото из списка', reply_markup=admin_photo_inlines(num-1, data[1], 'choice'))
        case 'choice':
            remove(f"photos/{data[2]}/{data[1]}.jpg")
            increase_num(data[2], -1)
            await call.message.answer('Готово')
            
    await call.answer()


# Main admin's command - pricelist management
async def check_pricelist_command(message: Message):
    """/check_pricelist command handler. Do the same as /pricelist command, but with admin's inline keys"""
    for i in await sql_pricelist_command():
        await message.answer_photo(FSInputFile(f'photos/{i[0]}/0.jpg'), caption=f'Название: {i[0]}\nОписание: {i[1]}\nЦена: {i[2]}₽',\
                reply_markup=admin_items_inlines(i[0]))


# Add states block
async def add_command(message: Message, state: FSMContext):
    """/add command handler. Start add_states machine"""
    await state.set_state(FSM_Admin.add_name)
    await message.reply('Введите название')

async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FSM_Admin.add_photo)
    await message.reply('Теперь отправьте фото')   

async def add_photo(message: Message, state: FSMContext):
    file_path = (await bot.get_file(message.photo[-1].file_id)).file_path
    mkdir(f"photos/{(await state.get_data())['name']}")
    await bot.download_file(file_path, f"photos/{(await state.get_data())['name']}/0.jpg")
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
    await message.answer_photo(FSInputFile(f"photos/{data['name']}/0.jpg"), \
        caption=f"Имя: {data['name']}\nОписание: {data['description']}\nЦена: {data['price']}₽")
    await state.clear()


# Compliting changes block
async def change_complite_text(message: Message, state: FSMContext):
    data = await state.get_data()
    await sql_change_command(data['name'], data['item'], message.text)
    await message.reply('Готово')
    await state.clear()

async def change_complite_photo(message: Message, state: FSMContext):
    file_path = (await bot.get_file(message.photo[-1].file_id)).file_path
    name = (await state.get_data())['name']
    num = (await get_num(name))[0][0]
    await increase_num(name, 1)
    rename(f"photos/{name}/0.jpg", f"photos/{name}/{num}.jpg")
    await bot.download_file(file_path, f"photos/{name}/0.jpg")
    await state.clear()


# Add more additional photos compliter
async def add_more_photos(message: Message, state: FSMContext):
    file_path = (await bot.get_file(message.photo[-1].file_id)).file_path
    name = (await state.get_data())['name']
    num = (await get_num(name))[0][0]
    await increase_num(name, 1)
    await bot.download_file(file_path, f"photos/{name}/{num}.jpg")
    await state.clear()
    await message.answer('Готово')



async def cancel_command(message: Message, state: FSMContext):
    """/cancel command handler. Cancel any state compliting"""
    if await state.get_state():
        await state.clear()
        await message.reply('OK')


def register_handlers_admin(dp: Dispatcher):
    """All admin's handlers register. Any admin's command besides /admin starts with AdminFilter which is\
        checking user to be in admins list"""
    dp.message.register(cancel_command, Command(commands='cancel'))

    dp.message.register(admin_command, Command(commands='admin'))
    dp.message.register(password_handler, FSM_Admin.password_check)

    dp.callback_query.register(admin_inlines, AdminFilter())
    dp.message.register(check_pricelist_command, Command(commands='check_pricelist'), AdminFilter())

    dp.message.register(add_command, Command(commands='add'), AdminFilter())
    dp.message.register(add_name, FSM_Admin.add_name)
    dp.message.register(add_photo, FSM_Admin.add_photo, F.photo)
    dp.message.register(add_description, FSM_Admin.add_description)
    dp.message.register(add_price, FSM_Admin.add_price)

    dp.message.register(add_more_photos, FSM_Admin.add_more_photos, F.photo)
    dp.message.register(change_complite_text, FSM_Admin.change_complite_text)
    dp.message.register(change_complite_photo, FSM_Admin.change_complite_photo, F.photo)