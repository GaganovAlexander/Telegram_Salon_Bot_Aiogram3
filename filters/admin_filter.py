from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from sqlite_db import get_admins_id


class AdminFilter(Filter):
    """Checks user to be in admins list"""
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in map(lambda x: int(x[0]), (await get_admins_id()))
    
    
class ClientInline(Filter):
    async def __call__(self, call: CallbackQuery):
        return 'photos' in call.data