from dataclasses import asdict
from pyrogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
)
from . import app, posts, datatypes, style


go_back = lambda data: [InlineKeyboardButton('« Go back', callback_data=data)]


@app.on_callback_query()
async def callback_handler(_, callback: CallbackQuery):
    args = callback.data.split()
    cmd = args[0]
    if cmd == 'menu':
        await menu(callback)
    elif cmd == 'deleteList':
        await delete_list(callback)
    elif cmd == 'delete':
        await delete_service(callback, int(args[1]))
    elif cmd == 'styleList':
        await style_list(callback)
    elif cmd == 'chooseStyle':
        await style_choose(callback, str(args[1]))
    elif cmd == 'setStyle':
        await style_set(callback, str(args[1]), int(args[2]))


async def menu(callback: CallbackQuery):
    await callback.edit_message_text(
        "Select an option:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Set post style", "styleList")],
            [InlineKeyboardButton("Delete a service", "deleteList")],
            [InlineKeyboardButton("Get informations", "getInformations")],
        ])
    )


async def style_list(callback: CallbackQuery):
    user = asdict(app.database.getUser(callback.message.chat.id))
    buttons = []
    for position in posts.Post.style:
        actual_style = style.getStyle(user[position+'_style'])
        buttons.append([InlineKeyboardButton(
            text=f"{position.title()} - {actual_style.name}",
            callback_data=f"chooseStyle {position}"
        )])
    buttons.append(go_back('menu'))
    await callback.edit_message_text(
        "Select the part of the post you want to select the style:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def style_choose(callback: CallbackQuery, position: str):
    buttons = list(map(
        lambda s: [InlineKeyboardButton(
            text=s.name,
            callback_data=f'setStyle {position} {s.id}'
        )],
        style.styles
    ))
    buttons.append(go_back('styleList'))
    await callback.edit_message_text(
        f"Choose one style for the {position}:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def style_set(callback: CallbackQuery, position: str, style_id: int):
    user_id = app.database.getUser(callback.message.chat.id).id
    app.database.updateUserStyle(
        user_id,
        datatypes.Style(**{position+'_style': style_id})
    )
    await callback.answer(f"Style for {position} updated!")
    await style_list(callback)


async def delete_list(callback: CallbackQuery):
    user_id = app.database.getUser(callback.message.chat.id).id
    services = app.database.getServicesOfUser(user_id)
    if not services:
        await callback.answer("You don't have any service registered!")
        try:
            await menu(callback)
        except Exception:
            pass
        return
    buttons = []
    for service in services:
        buttons.append([InlineKeyboardButton(
            text=service.title,
            callback_data=f'delete {service.id}'
        )])
    buttons.append(go_back('menu'))
    await callback.edit_message_text(
        "Choose a service:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def delete_service(callback: CallbackQuery, service_id: int):
    user_id = app.database.getUser(callback.from_user.id).id
    app.database.unlinkUserFromService(service_id, user_id)
    await callback.answer("Service removed!")
    await delete_list(callback)
