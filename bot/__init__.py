from dotenv import load_dotenv
from os import environ
from . import database
from pyrogram import Client


load_dotenv('.env')

RELOAD_DELAY = 120  # Time to await bettwen sending posts

app = Client(
    'RSS',
    api_id=int(environ.get('TELEGRAM_API_ID')),
    api_hash=environ.get('TELEGRAM_API_HASH'),
    bot_token=environ.get('BOT_TOKEN')
)

app.database = database.Controller(environ.get('DATABASE_URL'))
