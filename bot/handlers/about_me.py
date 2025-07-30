import os

from telethon import events
from bot.tools import get_keyboard, is_expected_steps
from bot.db_tools import _get_current_user_step, _update_current_user_step
from bot.bot_instance import bot


@bot.on(events.NewMessage(pattern="Обо мне 👾"))
async def about_me(event):
    user_id = event.message.peer_id.user_id
    step = await _get_current_user_step(user_id)

    if await is_expected_steps(user_id, [0]):
        await _update_current_user_step(user_id, 11)
        keyboard = await get_keyboard(["Назад"])
        text = (
            "Хэй!\n\nЯ бот, созданный с целью помочь определиться с выбором программы "
            "магистратуры ITMO"
        )
        await event.client.send_message(event.chat_id, text, buttons=keyboard)
