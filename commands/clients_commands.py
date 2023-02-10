from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


# List of all client's commands
client_commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='pricelist',
            description='Вывести прайс-лист'
        ),
    ]

async def set_client_commands(bot: Bot):
    """Sets up client's commands list"""
    await bot.set_my_commands(client_commands, BotCommandScopeDefault())