from time import time
from pyrogram.filters import command
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from feedparser import parse as FeedParse
from . import app


@app.on_message(command('start'))
async def start(_, msg: Message):
    await msg.reply(
        "Hello, I'm a bot to send you posts of your RSS services, " +
        "press 'Menu' button to open it",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Menu", callback_data="menu")],
            [InlineKeyboardButton("Source code", url="https://github.com/fortrax-br/atom-news")]
        ])
    )
    try:
        app.database.addUser(msg.chat.id)
    except Exception:
        pass


@app.on_message(command('add'))
async def add(_, msg: Message):
    msg_parts = msg.text.split()
    if len(msg_parts) == 1:
        await msg.reply("I need the URL of the service!")
        return
    url = msg_parts[1]
    service = FeedParse(url if '://' in url else 'http://'+url)
    if 'title' not in service.feed:
        await msg.reply("Failed to get informations about this service!")
        return
    service_title = service.feed.title.title()
    try:
        service_id = app.database.addService(service_title, service.href)
        app.database.setServiceLastUpdate(service_id, int(time()))
    except Exception:
        service_id = app.database.getService(service.href).id
    user_id = app.database.getUser(msg.chat.id).id
    already_linked = app.database.serviceAlreadyLinked(service_id, user_id)
    if already_linked:
        await msg.reply("The service is already added!")
        return
    app.database.linkServiceToUser(service_id, user_id)
    await msg.reply(f"Service __{service_title}__ added.", parse_mode="markdown")
