from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI

from tortoise.contrib.fastapi import register_tortoise
from os import getenv
from models import Crossing, User, Coords, Level, Image, Status

FSTR_DB_HOST = getenv("FSTR_DB_HOST")
FSTR_DB_PORT = getenv("FSTR_DB_PORT", "5432")
FSTR_DB_LOGIN = getenv("FSTR_DB_LOGIN")
FSTR_DB_PASS = getenv("FSTR_DB_PASS")

FSTR_DB_NAME = getenv("FSTR_DB_NAME", "pereval")

DB_URL = f"postgres://{FSTR_DB_LOGIN}:{FSTR_DB_PASS}@{FSTR_DB_HOST}:{FSTR_DB_PORT}/"

class CrossingsDB:
    def __init__(self, app: "FastAPI",  db_name: str):
        self.db_url = DB_URL + db_name
        register_tortoise(app, modules={"models": ["models"]}, db_url= self.db_url, generate_schemas=True)



    async def get_crossing(self, id: int):
        return await Crossing.get_or_none(id=id)


    async def try_to_add_crossing(self, payload: dict[str, ...]) -> bool | Crossing:
        try:
            if not (user := await User.get_or_none(email=payload["user"]["email"])):
                user = await User.create(**payload["user"])
            level = await Level.create(**payload["level"])
            coords = await Coords.create(**payload["coords"])
        except KeyError:
            return False

        images = payload.pop("images", [])

        payload["level"] = level
        payload["coords"] = coords
        payload["user"] = user

        payload["status"] = Status.NEW

        crossing = await Crossing.create(**payload)
        for image in images:
            await Image.create(**image, crossing=crossing)

        return crossing


