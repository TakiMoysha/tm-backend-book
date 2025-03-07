from enum import Enum
from typing import override
import peewee

from src.mixins import CreateUpdateModelMixin

DB = peewee.SqliteDatabase(":memory:")


class BaseModel(peewee.Model):
    class Meta:
        database = DB


## ============================================== Auth


class User(BaseModel, CreateUpdateModelMixin):
    email = peewee.CharField(unique=True)
    password = peewee.CharField(unique=True)
    is_activate = peewee.BooleanField(default=True)
    is_superuser = peewee.BooleanField(default=False)

    class Meta:
        indexes = ((("email", "password"), True),)


## ============================================== Community


class Member(BaseModel, CreateUpdateModelMixin):
    user = peewee.ForeignKeyField(User, backref="memberships")
    role = peewee.CharField()

    class Meta:
        indexes = ((("user_id", "role"), True),)


class Report(BaseModel, CreateUpdateModelMixin):
    user = peewee.ForeignKeyField(Member, backref="reports")
    text = peewee.TextField()
    # message =  # (?) OutboxMessage
    is_published = peewee.BooleanField(default=False)


class Group(BaseModel): ...


## ============================================== Enterprise


class Company(BaseModel, CreateUpdateModelMixin):
    id = peewee.UUIDField(primary_key=True)
    name = peewee.CharField()
    followed_user_id = peewee.IntegerField()
    group = peewee.ForeignKeyField(Group)

    class Meta:
        indexes = ((("name", "followed_user_id"), True),)


class Project(BaseModel, CreateUpdateModelMixin):
    id = peewee.UUIDField(primary_key=True)
    name = peewee.CharField()
    company = peewee.ForeignKeyField(Company)
    group = peewee.ForeignKeyField(Group)

    class Meta:
        indexes = ((("company_id", "group_id"), True),)


class CompanyRoles(Enum):
    OWNER = "Owner"  # Full Control
    PRINCIPAL = "Principal"  # Full Control
    ADMIN = "Admin"  # View, Edit, Create
    DEVELOPER = "Developer"  # View
    CONTRIBUTOR = "Contributor"  # View Allowed


class ProjectRoles(Enum):
    OWNER = "Owner"  # Create, Read, Update, Delete
    ADMIN = "Admin"  # Create, Read, Update
    DEVELOPER = "Developer"  # Read


class Permission(BaseModel): ...
