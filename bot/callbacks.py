from . import app, posts
from pyrogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
)


@app.on_callback_query()
async def callback_handler(_, callback: CallbackQuery):
    cmd = callback.data.split()
    if cmd[0] == 'menu':
        await menu(callback)
    elif cmd[0] == 'deleteList':
        await delete_list(callback)
    elif cmd[0] == 'delete':
        await delete_service(callback, int(cmd[1]))
    elif cmd[0] == 'styleList':
        await style_list(callback)
    elif cmd[0] == 'chooseStyle':
        await style_choose(callback, cmd[1])


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
    await callback.edit_message_text(
        "Select the part of the post you want to select the style:",
        reply_markup=InlineKeyboardMarkup(
            list(map(
                lambda v: [InlineKeyboardButton(
                    text=v.title(),
                    callback_data=f'chooseStyle {v}'
                )],
                posts.Post.style.keys()
            ))
        )
    )


async def style_choose(callback: CallbackQuery, position: str):
    lines = list(map(
        lambda style: [InlineKeyboardButton(
            text=style['name'],
            callback_data=f'setStyle {position} {posts.styles.index(style)}'
        )],
        posts.styles
    ))
    await callback.edit_message_text(
        f"Choose one style for the {position}:",
        reply_markup=InlineKeyboardMarkup(lines)
    )


async def style_set(callback: CallbackQuery, position: str, style: int):
    pass


async def delete_list(callback: CallbackQuery):
    user_id = app.database.getUser(callback.message.chat.id).id
    services = app.database.getServicesOfUser(user_id)
    lines = []
    for service in services:
        lines.append([
            InlineKeyboardButton(service.title, f'delete {service.id}')
        ])
    if len(lines) == 0:
        await callback.answer("You don't have any service registered!")
        try:
            await menu(callback)
        except Exception:
            pass
        return
    lines.append([InlineKeyboardButton("Go back", "menu")])
    await callback.edit_message_text(
        "Choose a service:",
        reply_markup=InlineKeyboardMarkup(lines)
    )


async def delete_service(callback: CallbackQuery, service_id: int):
    user_id = app.database.getUser(callback.from_user.id).id
    app.database.unlinkUserFromService(service_id, user_id)
    await callback.answer("Service removed!")
    await delete_list(callback)
