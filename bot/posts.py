from feedparser import FeedParserDict


styles = [
    { 'name': 'Normal',    'format': '{}' },
    { 'name': 'Italic',    'format': '<i>{}</i>' },
    { 'name': 'Bold',      'format': '<b>{}</b>' },
    { 'name': 'Monospace', 'format': '<pre>{}</pre>' },
    { 'name': 'Underline', 'format': '<u>{}</u>' },
    { 'name': 'Spoiler',   'format': '<tg-spoiler>{}</tg-spoiler>' },
]


def scapeString(text: str) -> str:
    characters = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
    for character, replace_by in characters.items():
        text = text.replace(character, replace_by)
    return text


class Post:
    style = {
        "title": styles[2]['format'],
        "service": styles[0]['format'],
        "description": styles[1]['format']
    }

    def __init__(self, service: str, post: FeedParserDict):
        self.service = service
        self.post = post

    def compile(self):
        text = f'<a href="{self.post.link}">'
        text += self.style['title'].format(scapeString(self.post.title))
        text += '</a>\n'  # Close title link
        text += self.style['service'].format(scapeString(self.service)) + "\n\n"
        if len(self.post.summary) >= 2048:
            description = self.post.summary[:2048] + "..."
        else:
            description = self.post.summary
        text += self.style['description'].format(scapeString(description))
        return text

    def setStyle(self, position: str, style: int):
        self.style[position] = styles[style]['format']
