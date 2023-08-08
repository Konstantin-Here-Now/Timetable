import json
import sqlite3
import os

from typing import Literal
from django.conf import settings
from main.models import AvailableTime

DB_PATH = os.path.join(settings.BASE_DIR, 'db.sqlite3')


def create_time_tables() -> None:
    at_data = settings.AVAILABLE_TIME
    AvailableTime.objects.create(time_type='default', at=at_data)
    AvailableTime.objects.create(time_type='actual', at=at_data)
    return None
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        query = f"""INSERT INTO main_availabletime VALUES
                ('default', '{json.dumps(settings.AVAILABLE_TIME)}'),
                ('actual', '{json.dumps(settings.AVAILABLE_TIME)}');"""
        cur.execute(query)


def get_available_time(time_type: Literal["default", "actual"]) -> dict[str, str]:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        query = f"SELECT * from main_availabletime WHERE time_type = '{time_type}';"
        cur.execute(query)
        result = json.loads(cur.fetchone()[1])
    return result


def set_default_time() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        query = f"""UPDATE main_availabletime SET at = '{json.dumps(settings.AVAILABLE_TIME)}'
                        WHERE time_type = 'default';"""
        cur.execute(query)
