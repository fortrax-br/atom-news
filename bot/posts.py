from feedparser import FeedParserDict
from bs4 import BeautifulSoup
from . import style
import textwrap


def scapeString(text: str) -> str:
    characters = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
    for character, replace_by in characters.items():
        text = text.replace(character, replace_by)
    return text


class Post:
    style = {
        "title": style.getStyle(2),
        "service": style.getStyle(0),
        "description": style.getStyle(1)
    }

    def __init__(self, title: str, link: str, service: str, summary: str):
        self.service = service
        self.link = link
        self.title = title.title()
        self.summary = summary

    def compile(self) -> str:
        title = scapeString(self.title.title())
        service = scapeString(self.service)
        complete_description = BeautifulSoup(self.summary, 'html.parser')
        description = textwrap.shorten(complete_description.getText(strip=True), 2048)
        description = scapeString(description)
        return textwrap.dedent(f'''
            <a href="{self.link}">{self.style['title'].template.format(title)}</a>
            {self.style['service'].template.format(service)}

            {self.style['description'].template.format(description)}
        ''')

    def setStyle(self, position: str, style_id: int):
        self.style[position] = style.getStyle(style_id)
