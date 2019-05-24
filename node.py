from __future__ import annotations
from typing import Generator, Sequence

from token import Token, TokenTypes


class Node:
    # Use this implementation of tree:
    # Every node has token from grammar and their children in list. The children
    # are sorted like in code from left to right from begin to end.
    def __init__(self, token: Token):
        self.token = token
        self.children = list()

    def add_child(self, token: Token) -> None:
        self.children.append(Node(token))

    def get_children(self, token_types: Sequence[TokenTypes]) -> \
            Generator[Node]:

        for child in self.children:
            if child.token.type in token_types:
                yield child

    def get_child(self, token_type: TokenTypes) -> Node:
        return next(self.get_children((token_type, )))
