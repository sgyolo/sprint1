from tortoise.models import Model, MetaInfo
from tortoise import fields, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from enum import StrEnum


class PydanticExlcudeIDModel(Model):
    class PydanticMeta:
        exclude = ("id",)


class Area(PydanticExlcudeIDModel):
    id = fields.IntField(pk=True)
    parent_id = fields.ForeignKeyField("models.Area")


class ActivityType(PydanticExlcudeIDModel):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=15)


class Image(PydanticExlcudeIDModel):
    class PydanticMeta:
        exclude = ("id", "date_added")

    id = fields.IntField(pk=True)
    date_added = fields.DatetimeField(auto_now_add=True)
    data = fields.BinaryField()
    title = fields.CharField(max_length=30)

    crossing = fields.ForeignKeyField(model_name="models.Crossing", related_name="images")


class Status(StrEnum):
    NEW = "new"
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Level(PydanticExlcudeIDModel):
    id = fields.IntField(pk=True)
    winter = fields.CharField(max_length=10)
    spring = fields.CharField(max_length=10)
    summer = fields.CharField(max_length=10)
    autumn = fields.CharField(max_length=10)


class User(PydanticExlcudeIDModel):
    id = fields.IntField(pk=True)
    email = fields.CharField(unique=True, max_length=30)
    phone = fields.CharField(max_length=14)
    fam = fields.CharField(max_length=30)
    name = fields.CharField(max_length=30)
    otc = fields.CharField(max_length=30)


class Crossing(PydanticExlcudeIDModel):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField("models.User", related_name="crossings")

    connect = fields.CharField(max_length=10)
    beauty_title = fields.CharField(max_length=30)
    title = fields.CharField(max_length=30)
    other_titles = fields.CharField(max_length=30)

    add_time = fields.DatetimeField()

    status = fields.CharEnumField(Status, default=Status.PENDING)

    level = fields.ForeignKeyField("models.Level", related_name="crossings")
    coords = fields.OneToOneField("models.Coords", related_name="crossing")


class Coords(PydanticExlcudeIDModel):
    id = fields.IntField(pk=True)
    latitude = fields.FloatField()
    longitude = fields.FloatField()
    height = fields.IntField()


Tortoise.init_models(["models"], "models")
CrossingPydantic = pydantic_model_creator(Crossing)

