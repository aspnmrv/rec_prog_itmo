from telethon import events
from bot.bot_instance import bot
from bot.db import get_ai_history, update_ai_messages_db
from bot.db_tools import _get_current_user_step
from bot.tools import get_keyboard, get_program_conversation


@bot.on(events.NewMessage)
async def ai_dialog(event):
    user_id = event.message.peer_id.user_id
    step = await _get_current_user_step(user_id)

    if step != 1:
        return

    user_message = event.raw_text.strip()

    await update_ai_messages_db(user_id, "user", user_message)

    history = await get_ai_history(user_id)
    bot_reply = await get_program_conversation(history, user_message)
    await update_ai_messages_db(user_id, "bot", bot_reply)
    keyboard = await get_keyboard(["Завершить"])
    await event.client.send_message(user_id, bot_reply, buttons=keyboard)
