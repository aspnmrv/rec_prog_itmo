from telethon import events

from bot.tools import get_keyboard
from bot.db_tools import _update_current_user_step, _create_db
from bot.db import is_user_exist_db, update_data_users_db, update_data_events_db
from bot.bot_instance import bot


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    print(event)
    sender_info = await event.get_sender()
    user_id = event.message.peer_id.user_id
    await _create_db()
    await _update_current_user_step(user_id, 0)
    if not await is_user_exist_db(user_id):
        await update_data_users_db(sender_info)

    keyboard = await get_keyboard(["Начать 🚀", "Обо мне 👾"])
    text = (
        "Hi! 👋\n\nПомогу разобраться с тем, какая программа ITMO тебе больше подходит "
        "и отвечу на твои вопросы по программам!"
    )
    await event.client.send_message(event.chat_id, text, buttons=keyboard)
    await update_data_events_db(user_id, "start", {"step": 0})
