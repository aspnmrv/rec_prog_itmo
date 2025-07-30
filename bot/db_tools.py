import ast
import sqlite3
import json
import os

from pathlib import Path

CONN = sqlite3.connect("sophie.db")


async def _create_db():
    """"""
    cur = CONN.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user_step_states
              (user_id INT, step INT)
        """
    )
    CONN.commit()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user_states_temp
              (user_id INT, states TEXT)
        """
    )
    CONN.commit()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user_msg_temp
              (user_id INT, msg TEXT)
        """
    )
    CONN.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_test_state
              (user_id INTEGER PRIMARY KEY, mode TEXT)
    """)
    CONN.commit()

    return


async def _get_current_user_step(user_id):
    cur = CONN.cursor()
    query = "SELECT step FROM user_step_states WHERE user_id = ?"
    cur.execute(query, (user_id,))
    data = cur.fetchall()
    CONN.commit()

    return int(data[0][0])


async def _truncate_table():
    cur = CONN.cursor()
    query = f"""
        DELETE FROM user_step_states
    """
    cur.execute(query)
    CONN.commit()
    return


async def _update_current_user_step(user_id: int, step: int):
    cur = CONN.cursor()
    query = "SELECT step FROM user_step_states WHERE user_id = ?"
    cur.execute(query, (user_id,))
    data = cur.fetchall()

    if len(data) == 0:
        query = "INSERT INTO user_step_states (user_id, step) VALUES (?, ?)"
        cur.execute(query, (user_id, step))
    else:
        query = "UPDATE user_step_states SET step = ? WHERE user_id = ?"
        cur.execute(query, (step, user_id))

    CONN.commit()
    return
