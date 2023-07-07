import asyncio

from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from os import getenv

FSTR_DB_HOST = getenv("FSTR_DB_HOST")
FSTR_DB_PORT = getenv("FSTR_DB_PORT", "5432")
FSTR_DB_LOGIN = getenv("FSTR_DB_LOGIN")
FSTR_DB_PASS = getenv("FSTR_DB_PASS")

FSTR_DB_NAME = getenv("FSTR_DB_NAME", "pereval")

DB_URL = f"postgres://{FSTR_DB_LOGIN}:{FSTR_DB_PASS}@{FSTR_DB_HOST}:{FSTR_DB_PORT}/"

async def init():


class CrossingsDB:
    def __init__(self, app: "FastAPI",  db_name: str):
        self.db_name = db_name
        register_tortoise(app, modules={"models": ["models"]}, db_url= DB_URL + db_name)

    async def add_crossing(self, payload):
        ...
