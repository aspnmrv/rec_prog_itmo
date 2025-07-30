from telethon import events

from bot.tools import is_expected_steps
from bot.handlers.start import start
from bot.handlers.begin import begin
from bot.db_tools import _get_current_user_step
from bot.bot_instance import bot


@bot.on(events.NewMessage(pattern="Назад"))
async def get_back(event):
    user_id = event.message.peer_id.user_id

    if await is_expected_steps(user_id, [11]):
        await start(event)
