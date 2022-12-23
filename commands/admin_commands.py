from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

from commands.clients_commands import client_commands

admin_commands = [
        BotCommand(
            command='add',
            description='Добавить пункт в прайс-лист'
        ),
        BotCommand(
            command='change',
            description='Изменить пункт прайс-листа'
        ),
        BotCommand(
            command='delete',
            description='Удалить пункт прайс-листа'
        ),
        BotCommand(
            command='cancel',
            description='Отменить выбор команды'
        ),
    ]

async def set_admin_commands(bot: Bot):
    await bot.set_my_commands(admin_commands+client_commands, BotCommandScopeDefault())