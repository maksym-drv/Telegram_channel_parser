from pyrogram import Client
import os

class Config:
    def __init__(self):
        self.host = os.environ.get('HOST')
        self.port = os.environ.get('PORT')
        self.username = os.environ.get('USER')
        self.passw = os.environ.get('PASS')

        self.database = os.environ.get('DATABASE')
        self.user_data = os.environ.get('DATA_USER')
        self.password_data = os.environ.get('DATA_PASS')
        self.host_data = os.environ.get('HOST')
        self.port_data = os.environ.get('DATA_PORT')

        self.parser = Client(
            "tg_parser", 
            os.environ.get('API_ID'), 
            os.environ.get('API_HASH')
        )
        
        self.delay = int(os.environ.get('DELAY'))