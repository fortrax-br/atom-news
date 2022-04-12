from . import app
from time import time
from pyrogram import Client
from pyrogram.filters import command
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from feedparser import parse as FeedParse


@app.on_message(command('start'))
async def start(app: Client, msg: Message):
    await msg.reply(
        "Hello, I'm a bot to send you posts of your RSS services, " +
        "press 'Menu' button to open it",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Menu", callback_data="menu")],
            [InlineKeyboardButton("Source code", url="https://github.com/fortrax-br")]
        ])
    )
    try: app.database.addUser(msg.chat.id)
    except: pass


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
    except:
        service_id = app.database.getService(service.href).id
    user_id = app.database.getUser(msg.chat.id).id
    alreadyLinked = app.database.serviceAlreadyLinked(service_id, user_id)
    if alreadyLinked:
        await msg.reply("The service is already added!")
        return
    app.database.linkServiceToUser(service_id, user_id)
    await msg.reply(f"Service __{service_title}__ added.", parse_mode="markdown")


@app.on_message(command('del'))
async def delete(_, msg: Message):
    user_id = app.database.getUser(msg.chat.id).id
    services = app.database.getServicesOfUser(user_id)
    rows = []
    for service in services:
        rows.append([
            InlineKeyboardButton(service.title, callback_data=f'del {service.id}')
        ])
    if len(rows) == 0:
        await msg.reply("You don't have any service registered!")
    else:
        await msg.reply("Choose a service:", reply_markup=InlineKeyboardMarkup(rows))
