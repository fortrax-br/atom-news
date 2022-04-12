from . import app
from pyrogram import Client
from pyrogram.types import CallbackQuery


@app.on_callback_query()
async def callback_handler(_, callback: CallbackQuery):
    cmd, data = callback.data.split()
    if cmd == 'del':
        await delete_service(callback, int(data))


async def delete_service(callback: CallbackQuery, service_id: int):
    user_id = app.database.getUser(callback.from_user.id).id
    app.database.unlinkUserFromService(service_id, user_id)
    await callback.edit_message_text("Service removed!")
