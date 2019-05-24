from __future__ import annotations
from typing import Iterable

from token import Token


class Node:
    def __init__(self, token: Token):
        self.token = token
        self.children = list()

    def add_child(self, token: Token) -> None:
        self.children.append(Node(token))

    def get_children(self) -> Iterable[Node]:
        for child in self.children:
            yield child
