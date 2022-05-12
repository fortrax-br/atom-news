from dataclasses import dataclass


@dataclass
class Style:
    name: str
    template: str
    id: int


styles = [
    Style('Normal', '{}', 0),
    Style('Italic', '<i>{}</i>', 1),
    Style('Bold', '<b>{}</b>', 2),
    Style('Monospace', '<pre>{}</pre>', 3),
    Style('Underline', '<u>{}</u>', 4),
    Style('Spoiler', '<tg-spoiler>{}</tg-spoiler>', 5)
]


def getStyle(id: int) -> Style | None:
    style = list(map(lambda style: style.id == id, styles))
    if not style:
        return None
    return style[0]
