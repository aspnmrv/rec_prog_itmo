from telethon import events

from bot.tools import get_keyboard
from bot.db_tools import _update_current_user_step, _create_db
from bot.db import is_user_exist_db, update_data_users_db
from bot.bot_instance import bot


@bot.on(events.NewMessage(pattern="Завершить"))
async def start(event):
    user_id = event.message.peer_id.user_id

    keyboard = await get_keyboard(["Начать 🚀"])
    text = (
        "Хорошо! Надеюсь, что помог!"
    )
    await event.client.send_message(event.chat_id, text, buttons=keyboard)
    await _update_current_user_step(user_id, 3)
