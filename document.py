from typing import Set


class Document:
    body: str

    def __init__(self, title: str, body: str):
        self.body = body
        self.dish = title

    def __str__(self) -> str:
        return f'{self.dish}: {self.body}'

    def words(self) -> Set[str]:
        words_list = self.body.split(" ")
        return set(words_list)
