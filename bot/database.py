import sqlalchemy as sql
from typing import List
from . import datatypes
from dataclasses import asdict


class Controller:
    def __init__(self, url: str):
        self.engine = sql.create_engine(url, echo=False)
        meta = sql.MetaData(self.engine)
        self.users = sql.Table(
            "users", meta,
            sql.Column(
                "id", sql.Integer,
                primary_key=True, autoincrement=True
            ),
            sql.Column("chat_id", sql.BigInteger, unique=True),
            sql.Column("title_style", sql.Integer, server_default="2"),
            sql.Column("service_style", sql.Integer, server_default="0"),
            sql.Column("description_style", sql.Integer, server_default="1"),
        )
        self.services = sql.Table(
            "services", meta,
            sql.Column(
                "id", sql.Integer,
                primary_key=True, autoincrement=True
            ),
            sql.Column("url", sql.String(2048), unique=True),
            sql.Column("title", sql.String(2048)),
            sql.Column("last_update", sql.BigInteger)
        )
        self.linked = sql.Table(
            "linked", meta,
            sql.Column("user_id", sql.ForeignKey(self.users.c.id)),
            sql.Column("service_id", sql.ForeignKey(self.services.c.id))
        )
        meta.create_all()

    def addUser(self, chat_id: int) -> int:
        cmd = self.users.insert().values(chat_id=chat_id)
        return cmd.execute().inserted_primary_key[0]

    def getUser(self, chat_id: int) -> datatypes.User:
        try:
            self.addUser(chat_id)
        except Exception:
            pass
        query = self.users.select().where(self.users.c.chat_id == chat_id)
        user = query.execute().fetchone()
        return datatypes.User(*user)

    def updateUserStyle(self, user_id: int, style: datatypes.Style):
        raw = asdict(style)
        modified = dict(filter(lambda p: p[1] != None, raw.items()))
        cmd = self.users.update().values(**modified).where(
            self.users.c.id == user_id
        )
        cmd.execute()

    def addService(self, title: str, url: str) -> int:
        cmd = self.services.insert().values(title=title, url=url)
        return cmd.execute().inserted_primary_key[0]

    def getService(self, service_url: str) -> datatypes.Service:
        query = self.services.select().where(
            self.services.c.url == service_url
        )
        service = query.execute().fetchone()
        return datatypes.Service(*service)

    def setServiceLastUpdate(self, service_id: int, update: int):
        self.services.update().values(last_update=update).where(
            self.services.c.id == service_id
        ).execute()

    def getAllServices(self) -> List[datatypes.Service]:
        query = self.services.select()
        services = query.execute().fetchall()
        return list(map(lambda service: datatypes.Service(*service), services))

    def getUsersOfService(self, service_id: int) -> List[datatypes.User]:
        query = self.users.select().where(
            self.linked.c.user_id == self.users.c.id,
            self.linked.c.service_id == self.services.c.id,
            self.services.c.id == service_id
        )
        users = query.execute().fetchall()
        return list(map(lambda user: datatypes.User(*user), users))

    def getServicesOfUser(self, user_id: int) -> List[datatypes.Service]:
        query = self.services.select().where(
            self.linked.c.user_id == self.users.c.id,
            self.linked.c.service_id == self.services.c.id,
            self.users.c.id == user_id
        )
        services = query.execute().fetchall()
        return list(map(lambda service: datatypes.Service(*service), services))

    def linkServiceToUser(self, service_id: int, user_id: int):
        cmd = self.linked.insert().values(
            service_id=service_id, user_id=user_id
        )
        cmd.execute()

    def serviceAlreadyLinked(self, service_id: int, user_id: int) -> bool:
        query = self.linked.select().where(
            self.linked.c.user_id == user_id,
            self.linked.c.service_id == service_id
        )
        result = query.execute().fetchone()
        return True if result is not None else False

    def unlinkUserFromService(self, service_id: int, user_id: int):
        cmd = self.linked.delete().where(
            self.linked.c.service_id == service_id,
            self.linked.c.user_id == user_id
        )
        cmd.execute()
