import os
import sys

sys.path.append(os.path.dirname(__file__))
sys.path.insert(1, os.path.realpath(os.path.pardir))

import psycopg2
import json

from psycopg2 import pool
from psycopg2.extras import execute_values
from globals import MINCONN, MAXCONN
from datetime import datetime
from functools import wraps
from datetime import datetime
from typing import Callable


def connect_from_config(file):
    keepalive_kwargs = {
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 5,
        "keepalives_count": 5,
    }
    with open(file, 'r') as fp:
        config = json.load(fp)
    return psycopg2.connect(**config, **keepalive_kwargs)


def create_pool_from_config(minconn, maxconn, file):
    with open(file, 'r') as fp:
        config = json.load(fp)
    return pool.SimpleConnectionPool(minconn, maxconn, **config)


CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "config", "config.json")
GLOBAL_POOL = create_pool_from_config(MINCONN, MAXCONN, CONFIG_PATH)


def reconnect():
    """"""
    global CONN_GLOBAL
    if CONN_GLOBAL.closed == 1:
        CONN_GLOBAL = connect_from_config(CONFIG_PATH)


async def is_exist_temp_db(table_name: str, user_id: int, field: str = "user_id") -> bool:
    conn = GLOBAL_POOL.getconn()
    cur = conn.cursor()
    query = f"""
        SELECT {field}
        FROM {table_name}
        WHERE {field} = %s
    """
    cur.execute(query, (user_id,))
    data = cur.fetchall()
    GLOBAL_POOL.putconn(conn)
    return bool(data)


async def is_user_exist_db(user_id: int) -> bool:
    conn = GLOBAL_POOL.getconn()
    cur = conn.cursor()
    query = """
        SELECT id
        FROM public.users
        WHERE id = %s
    """
    cur.execute(query, (user_id,))
    data = cur.fetchall()
    GLOBAL_POOL.putconn(conn)
    return bool(data)


async def update_data_users_db(data) -> None:
    id = data.id
    first_name = data.first_name
    last_name = data.last_name
    is_bot = data.bot
    premium = data.premium
    username = data.username
    lang = data.lang_code
    scam = data.scam
    access_hash = data.access_hash
    phone = data.phone
    created_at = datetime.now()

    conn = GLOBAL_POOL.getconn()
    cur = conn.cursor()
    query = """
        INSERT INTO public.users 
            (id, created_at, first_name, last_name, is_bot, username, lang, scam, access_hash, phone, premium)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(query, (id, created_at, first_name, last_name, is_bot, username, lang, scam, access_hash, phone, premium))
    conn.commit()
    GLOBAL_POOL.putconn(conn)


async def update_ai_messages_db(user_id, from_, text):
    conn = GLOBAL_POOL.getconn()
    cur = conn.cursor()
    created_at = datetime.now()
    cur.execute("""
        INSERT INTO public.ai_dialog_messages (created_at, user_id, from_, text)
        VALUES (%s, %s, %s, %s)
    """, (created_at, user_id, from_, text))
    conn.commit()
    GLOBAL_POOL.putconn(conn)


async def get_ai_history(user_id):
    conn = GLOBAL_POOL.getconn()
    cur = conn.cursor()
    cur.execute("""
        SELECT from_, text FROM public.ai_dialog_messages
        WHERE user_id = %s ORDER BY created_at ASC
    """, (user_id,))
    rows = cur.fetchall()
    GLOBAL_POOL.putconn(conn)
    history = []
    for from_, text in rows:
        role = "assistant" if from_ == "bot" else "user"
        history.append({"role": role, "content": text})
    return history
