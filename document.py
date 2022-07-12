from typing import Set


class Document:
    title: str
    body: str

    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body

    def __str__(self) -> str:
        return f'{self.title}: {self.body}'

    def words(self) -> Set[str]:
        words_list = self.body.split(" ")
        return set(words_list)
