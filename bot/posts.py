from typing import Dict
from feedparser import FeedParserDict
from bs4 import BeautifulSoup
from . import style


def scapeString(text: str) -> str:
    characters = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
    for character, replace_by in characters.items():
        text = text.replace(character, replace_by)
    return text


class Post:
    style: Dict[str, style.Style] = {
        "title": style.getStyle(2),
        "service": style.getStyle(0),
        "description": style.getStyle(1)
    }

    def __init__(self, service: str, post: FeedParserDict):
        self.service = service
        self.post = post

    def compile(self):
        text = f'<a href="{self.post.link}">'
        text += self.style['title'].template.format(scapeString(self.post.title))
        text += '</a>\n'  # Close title link
        text += self.style['service'].template.format(scapeString(self.service)) + "\n\n"
        if len(self.post.summary) >= 2048:
            raw_description = self.post.summary[:2048] + "..."
        else:
            raw_description = self.post.summary
        description = BeautifulSoup(markup=raw_description, features='html.parser')
        text += self.style['description'].template.format(scapeString(description.getText(strip=True)))
        return text

    def setStyle(self, position: str, style_id: int):
        self.style[position] = style.getStyle(style_id)
