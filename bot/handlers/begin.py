from telethon import events

from bot.tools import get_keyboard, is_expected_steps, get_program_conversation
from bot.db_tools import (
    _update_current_user_step,
    _get_current_user_step
)
from bot.db import get_ai_history, update_ai_messages_db
from telethon.tl.custom import Button
from bot.bot_instance import bot


@bot.on(events.NewMessage(pattern="Начать 🚀"))
async def begin(event):
    user_id = event.message.peer_id.user_id
    step = await _get_current_user_step(user_id)

    if await is_expected_steps(user_id, [0, 3]):
        await _update_current_user_step(user_id, 1)
        text = "Начнем! Спрашивай меня любые вопросы, а я постараюсь тебе помочь " \
               "с ответами 🙂\n\nКогда устанешь, нажимай на кнопку Завершить!\n\n"
        keyboard = await get_keyboard(["Завершить"])
        await event.client.send_message(event.sender_id, text, buttons=keyboard)

        history = await get_ai_history(user_id)
        bot_reply = await get_program_conversation(history, "")
        await update_ai_messages_db(user_id, "bot", bot_reply)
        keyboard = await get_keyboard(["Завершить"])
        await event.client.send_message(user_id, bot_reply, buttons=keyboard)
