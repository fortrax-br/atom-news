from . import app
from pyrogram import Client
from pyrogram.types import (
    CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
)


@app.on_callback_query()
async def callback_handler(_, callback: CallbackQuery):
    cmd = callback.data.split()
    if cmd[0] == 'menu':
        await menu(callback)
    if cmd[0] == 'deleteList':
        await delete_list(callback)
    elif cmd[0] == 'delete':
        await delete_service(callback, int(cmd[1]))


async def menu(callback: CallbackQuery):
    await callback.edit_message_text(
        "Select an option:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Set post style", "setStyle")],
            [InlineKeyboardButton("Delete a service", "deleteList")],
            [InlineKeyboardButton("Get informations", "getInformations")],
        ])
    )


async def delete_list(callback: CallbackQuery):
    user_id = app.database.getUser(callback.message.chat.id).id
    services = app.database.getServicesOfUser(user_id)
    rows = []
    for service in services:
        rows.append([
            InlineKeyboardButton(service.title, f'delete {service.id}')
        ])
    if len(rows) == 0:
        await callback.answer("You don't have any service registered!")
        try: await menu(callback)
        except: pass
        return
    rows.append([InlineKeyboardButton("Go back", "menu")])
    await callback.edit_message_text("Choose a service:", reply_markup=InlineKeyboardMarkup(rows))


async def delete_service(callback: CallbackQuery, service_id: int):
    user_id = app.database.getUser(callback.from_user.id).id
    app.database.unlinkUserFromService(service_id, user_id)
    await callback.answer("Service removed!")
    await delete_list(callback)
