from aiogram import Bot, Dispatcher
from os import getenv


bot = Bot(token=getenv('TOKEN'), parse_mode='HTML')
dp = Dispatcher()