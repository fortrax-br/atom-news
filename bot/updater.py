from . import app, datatypes, RELOAD_DELAY
from .posts import Post
from time import sleep, mktime
from pyrogram import Client
from typing import List
from threading import Thread
import feedparser


def run():
    while True:
        verifyUpdates(app)
        sleep(RELOAD_DELAY)


def verifyUpdates(app: Client):
    services = app.database.getAllServices()
    for service in services:
        users = app.database.getUsersOfService(service.id)
        if len(users) == 0:
            continue
        update = feedparser.parse(service.url, sanitize_html=True)
        raw_posts = []
        for post in update.entries:
            if mktime(post['updated_parsed']) <= service.last_update:
                break
            raw_posts.append(post)
        if len(raw_posts) == 0:
            continue
        raw_posts.reverse()
        for user in users:
            Thread(
                target=sendPostsToUser,
                args=(user, update.feed.title, raw_posts)
            ).start()
        app.database.setServiceLastUpdate(
            service.id,
            int(mktime(raw_posts[-1]['updated_parsed']))
        )


def sendPostsToUser(user: datatypes.User, service_title: str, posts: List[dict]):
    for raw_post in posts:
        post = Post(service_title, raw_post)
        post.setTitleStyle(user.title_style)
        post.setServiceNameStyle(user.service_style)
        post.setDescriptionStyle(user.description_style)
        app.send_message(user.chat_id, post.compile(), parse_mode="html")
        sleep(1)
