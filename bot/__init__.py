from dotenv import load_dotenv
from pyrogram import Client
from os import environ
from . import database

load_dotenv('.env')

# Constants
RELOAD_DELAY = 120

app = Client(
    'RSS',
    api_id=environ.get('TELEGRAM_API_ID'),
    api_hash=environ.get('TELEGRAM_API_HASH'),
    bot_token=environ.get('BOT_TOKEN')
)

app.database = database.Controller(environ.get('DATABASE_URL'))
