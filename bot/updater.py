from typing import List, Callable
from threading import Thread
from time import sleep, mktime
from pyrogram.enums import ParseMode
import feedparser
from . import app, datatypes, RELOAD_DELAY
from .posts import Post


def run(stop: Callable):
    verifyUpdates()
    counter = 0
    while not stop():
        if counter == RELOAD_DELAY:
            verifyUpdates()
            counter = 0
        sleep(1)
        counter += 1


def verifyUpdates():
    services = app.database.getAllServices()
    for service in services:
        users = app.database.getUsersOfService(service.id)
        if not users:
            continue
        update = feedparser.parse(service.url, sanitize_html=True)
        raw_posts = []
        for post in update.entries:
            if mktime(post['updated_parsed']) <= service.last_update:
                break
            raw_posts.append(post)
        if not raw_posts:
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
    for post in posts:
        post = Post(post.title, post.link, service_title, post.summary)
        post.setStyle('title', user.title_style)
        post.setStyle('service', user.service_style)
        post.setStyle('description', user.description_style)
        try:
            app.send_message(user.chat_id, post.compile(), parse_mode=ParseMode.HTML)
        except Exception as error:
            print(f"Error sending post to {user.chat_id}: {error}")
            break
        sleep(1.2)
