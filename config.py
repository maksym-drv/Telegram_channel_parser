from aiogram import Bot, Dispatcher
from json_data import Buffer, Users, Words
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

class Config:
    def __init__(self):
        self.bot = Bot(token=os.environ.get('TELEGRAM_TOKEN'))
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())

        self.buffer = Buffer(file=os.environ.get('BUFFER'))
        self.users = Users(file=os.environ.get('USERS'))
        self.words = Words(file=os.environ.get('WORDS'))

        self.host = os.environ.get('HOST')
        self.port = os.environ.get('PORT')
        self.username = os.environ.get('USER')
        self.passw = os.environ.get('PASS')

        self.database = os.environ.get('DATABASE')
        self.user_data = os.environ.get('DATA_USER')
        self.password_data = os.environ.get('DATA_PASS')
        self.host_data = os.environ.get('HOST')
        self.port_data = os.environ.get('DATA_PORT')