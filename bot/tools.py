from telethon.tl.custom import Button
from typing import List, Literal, Tuple, Dict, Optional, Any
from db_tools import _get_current_user_step


async def get_keyboard(text_keys: List[str]) -> List[List[Button]]:
    """"""
    keyboard = list()
    for key in range(len(text_keys)):
        keyboard.append([Button.text(text_keys[key], resize=True)])
    return keyboard


async def is_expected_steps(user_id: int, expected_steps: List[Any]) -> bool:
    """Checking if a user exists in certain steps"""

    current_step = await _get_current_user_step(user_id)

    if current_step in expected_steps:
        return True
    else:
        return False
