from telethon import events

from bot.tools import get_keyboard, is_expected_steps
from bot.db_tools import (
    _update_current_user_step,
    _get_current_user_step
)
from telethon.tl.custom import Button
from bot.bot_instance import bot


@bot.on(events.NewMessage(pattern="Начать 🚀"))
async def begin(event):
    user_id = event.message.peer_id.user_id
    step = await _get_current_user_step(user_id)

    if await is_expected_steps(user_id, [0]):
        await _update_current_user_step(user_id, 1)
        text = "Начнем!"
        keyboard = await get_keyboard(["Завершить"])
        await event.client.send_message(event.sender_id, text, buttons=keyboard)
