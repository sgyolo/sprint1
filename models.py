from tortoise.models import Model
from tortoise import fields
import tortoise.models

from enum import StrEnum

class Area(Model):
    id = fields.IntField(pk=True)
    parent_id = fields.ForeignKeyField("models.Area")


class ActivityType(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=15)



class CrossingImage(Model):
    id = fields.IntField(pk=True)
    crossing = fields.ForeignKeyRelation("models.Crossing")
    image = fields.ForeignKeyRelation("models.Image")

class Image(Model):
    id = fields.IntField(pk=True)
    date_added = fields.DatetimeField(auto_now_add=True)
    img = fields.BinaryField()

class Status(StrEnum):
    NEW = "new"
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class Level(Model):
    winter = fields.CharField(max_length=10)
    spring = fields.CharField(max_length=10)
    summer = fields.CharField(max_length=10)
    autumn = fields.CharField(max_length=10)

class Crossing(Model):
    id = fields.IntField(pk=True)

    user = fields.ForeignKeyField("models.User", related_name="crossings")
    connect = fields.CharField(max_length=10)

    beauty_title = fields.CharField(max_length=30)
    title = fields.CharField(max_length=30)

    add_time = fields.DatetimeField(auto_now_add=True)

    level = fields.OneToOneField("models.Level")
    coord_id = fields.OneToOneField("models.Coords", related_name="crossing")


class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(unique=True, max_length=30)
    phone = fields.CharField(max_length=14)
    fam = fields.CharField(max_length=30)
    name = fields.CharField(max_length=30)
    otc = fields.CharField(max_length=30)


class Coords(Model):
    coord_id = fields.IntField(pk=True)
    latitude = fields.FloatField()
    longitude = fields.FloatField()
    height = fields.IntField()
