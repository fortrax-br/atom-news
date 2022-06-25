from typing import List
from dataclasses import asdict
import sqlalchemy as sql
from . import datatypes


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
            sql.Column("title_style", sql.Integer, server_default="1"),
            sql.Column("service_style", sql.Integer, server_default="0"),
            sql.Column("description_style", sql.Integer, server_default="3"),
        )
        self.services = sql.Table(
            "services", meta,
            sql.Column(
                "id", sql.Integer,
                primary_key=True, autoincrement=True
            ),
            sql.Column("url", sql.Text, unique=True),
            sql.Column("title", sql.Text),
            sql.Column("last_update", sql.BigInteger)
        )
        self.linked = sql.Table(
            "linked", meta,
            sql.Column("user_id", sql.ForeignKey(self.users.c.id)),
            sql.Column("service_id", sql.ForeignKey(self.services.c.id))
        )
        meta.create_all()

    def addUser(self, chat_id: int) -> int:
        "Add a normal user with default values and return they id"
        cmd = self.users.insert().values(chat_id=chat_id)
        return cmd.execute().inserted_primary_key[0]

    def getUser(self, chat_id: int) -> datatypes.User:
        "Get a user(create it if not exists) based on the chat id"
        try:
            self.addUser(chat_id)  # Create the user if not exists
        except Exception:
            pass
        query = self.users.select().where(self.users.c.chat_id == chat_id)
        user = query.execute().fetchone()
        return datatypes.User(*user)

    def updateUserStyle(self, chat_id: int, style: datatypes.Style):
        "Set the post style to be used"
        raw = asdict(style)
        modified = dict(filter(lambda p: p[1] != None, raw.items()))  # Filter the non empty values
        cmd = self.users.update().values(**modified).where(
            self.users.c.chat_id == chat_id
        )
        cmd.execute()

    def addService(self, title: str, url: str) -> int:
        "Add a service to the database to be linked to many users at the same time"
        cmd = self.services.insert().values(title=title, url=url)
        return cmd.execute().inserted_primary_key[0]

    def getService(self, service_url: str) -> datatypes.Service:
        "Get only a service based on the URL"
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

    def getServicesOfUser(self, chat_id: int) -> List[datatypes.Service]:
        query = self.services.select().where(
            self.linked.c.user_id == self.users.c.id,
            self.linked.c.service_id == self.services.c.id,
            self.users.c.chat_id == chat_id
        )
        services = query.execute().fetchall()
        return list(map(lambda service: datatypes.Service(*service), services))

    def linkServiceToUser(self, service_id: int, chat_id: int):
        cmd = self.linked.insert().values(
            service_id=service_id,
            user_id=self.getUser(chat_id).id
        )
        cmd.execute()

    def serviceAlreadyLinked(self, service_id: int, chat_id: int) -> bool:
        query = self.linked.select().where(
            self.linked.c.user_id == self.users.c.id,
            self.linked.c.service_id == service_id,
            self.users.c.chat_id == chat_id
        )
        result = query.execute().fetchone()
        return True if result is not None else False

    def unlinkUserFromService(self, chat_id: int, service_id: int):
        cmd = self.linked.delete().where(
            self.linked.c.service_id == service_id,
            self.linked.c.user_id == self.getUser(chat_id).id
        )
        cmd.execute()
