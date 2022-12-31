from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from commands.clients_commands import client_commands

# List of all admins commands
admin_commands = [
        BotCommand(
            command='add',
            description='Добавить пункт в прайс-лист'
        ),
        BotCommand(
            command='check_pricelist',
            description='Вывести прайс-лист с функциями администратора'
        ),
        BotCommand(
            command='cancel',
            description='Отменить выбор команды'
        ),
    ]

async def set_admin_commands(bot: Bot):
    """Sets up admins commands list"""
    await bot.set_my_commands(admin_commands+client_commands, BotCommandScopeDefault())