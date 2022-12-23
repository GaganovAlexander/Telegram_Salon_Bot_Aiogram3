from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

client_commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='help',
            description='Вывести список всех комманд'
        ),
        BotCommand(
            command='pricelist',
            description='Вывести прайс-лист'
        ),
        BotCommand(
            command='address',
            description='Узнать адрес'
        ),
        BotCommand(
            command='get_contacts',
            description='Узнать контакты для связи'
        )
    ]

async def set_client_commands(bot: Bot):
    await bot.set_my_commands(client_commands, BotCommandScopeDefault())