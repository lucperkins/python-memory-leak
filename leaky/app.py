from typing import List
import logging
from random import choice

from flask import Flask

app = Flask(__name__)


class Todo(object):
    def __init__(self, id: int, task: str, done: bool = False) -> None:
        self.id = id
        self.task = task
        self.done = done


class User(object):
    def __init__(self, id: int, name: str, todos: List[Todo] = []) -> None:
        self.id = id
        self.name = name
        self.todos = todos

    def __del__(self) -> None:
        if self.todos != []:
            self.todos = []


tasks: List[str] = [
    'Pick something up from the store',
    'Buy an anniversary gift',
]

names: List[str] = [
    'Tom',
    'Jerry',
]


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    app.run()


if __name__ == '__main__':
    main()
