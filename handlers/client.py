from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.filters import Command


async def start_command(message: Message):
    await message.answer(f'{message.from_user.full_name}, здравствуйте!')

def register_handlers_client(dp: Dispatcher):
    dp.message.register(start_command, Command(commands=['start']))