class Post:
    style = {
        "title": "**",
        "service": "",
        "description": "__"
    }
    def __init__(self, service: str, post: dict):
        self.service = service
        self.post = post

    def compile(self):
        text = self.style['title'].format(scapeString("Service: " + self.post.title)) + "\n"
        text += self.style['service'].format(scapeString(self.service)) + "\n\n"
        if len(self.post.summary) >= 2048:
            description = self.post.summary[:2048] + "..."
        else:
            description = self.post.summary
        text += self.style['description'].format(scapeString(description)) + '\n\n'
        text += f"<a href=\"{self.post.link}\">Read more...</a>"
        return text

    def setTitleStyle(self, style: int):
        self.style['title'] = chooseStyleString(style)

    def setServiceNameStyle(self, style: int):
        self.style['service'] = chooseStyleString(style)

    def setDescriptionStyle(self, style: int):
        self.style['description'] = chooseStyleString(style)


def chooseStyleString(style: int) -> str:
    if style == 0:   # Normal
        return "{0}"
    elif style == 1: # Italic
        return "<i>{0}</i>"
    elif style == 2: # Bold
        return "<b>{0}</b>"
    elif style == 3: # Monospace
        return "<pre>{0}</pre>"
    elif style == 4: # Underline
        return "<u>{0}</u>"
    elif style == 5: # Spoiler
        return "<tg-spoiler>{0}</tg-spoiler>"


def scapeString(text: str) -> str:
    characters = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
    for c, r in characters.items():
        text = text.replace(c, r)
    return text
