from os import getenv

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from create_bot import bot


class AdminFilter(Filter):
    """Checks user to be in admins list"""
    async def __call__(self, message: Message) -> bool:
        return (await bot.get_chat_member(getenv('CHAT_ID'), message.from_user.id)).status != 'left'
    
    
class ClientInline(Filter):
    async def __call__(self, call: CallbackQuery):
        return 'photos' in call.data or '0pricelist' in call.data or 'book' in call.data