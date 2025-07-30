import openai
import json

from telethon.tl.custom import Button
from typing import List, Literal, Tuple, Dict, Optional, Any
from db_tools import _get_current_user_step

from config import config

from typing import List, Dict, Optional
from globals import MODEL, TEMPERATURE, MAX_TOKENS


openai.api_key = config.api_key


model = MODEL

with open("programs.json", "r", encoding="utf-8") as f:
    PROGRAMS_CONTEXT = json.load(f)


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


async def get_program_conversation(history: list, message: str) -> str:
    """
    """

    programs_text = []
    for key, prog in PROGRAMS_CONTEXT.items():
        courses_str = "\n".join([f"{c['semester']}: {c['name']} ({c['credits']} кр., {c['hours']} ч.)"
                                 for c in prog.get("courses", [])])
        programs_text.append(
            f"Программа: {prog['program_name']}\nОписание: {prog['description']}\nКурсы:\n{courses_str}"
        )
    programs_context_text = "\n\n".join(programs_text)

    system_prompt = f"""Ты — помощник для абитуриента, который выбирает между магистратурами ИТМО:
1) "Искусственный интеллект"
2) "Управление ИИ-продуктами"

Вот описание и учебные планы программ:
{programs_context_text}

Твоя задача — вести диалог, помогать разобраться, задавать наводящие вопросы про интересы пользователя
(хочет ли он заниматься исследованиями, кодингом и ML или больше управлением продуктами, бизнесом и стратегией).
Держи разговор дружелюбным, задавай уточняющие вопросы, не отвечай односложно.
В конце разговора предложи рекомендацию: какая программа лучше подходит.
"""

    messages = [{"role": "system", "content": system_prompt}]
    messages += history
    messages.append({"role": "user", "content": message})

    resp = await openai.ChatCompletion.acreate(
        model=model,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    return resp["choices"][0]["message"]["content"]
