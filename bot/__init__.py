from os import environ
from dotenv import load_dotenv
from pyrogram import Client
from . import database


load_dotenv('.env')

RELOAD_DELAY = 120  # Time to await bettwen sending posts

app = Client(
    'RSS',
    api_id=int(environ.get('TELEGRAM_API_ID')),
    api_hash=environ.get('TELEGRAM_API_HASH'),
    bot_token=environ.get('BOT_TOKEN')
)

app.database = database.Controller(environ.get('DATABASE_URL'))
