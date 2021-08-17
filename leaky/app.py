from typing import List, Type
import logging

from flask import Flask, jsonify, request, Response

app = Flask(__name__)


class Jsonable(object):
    def to_dict(self) -> dict:
        pass


class Todo(Jsonable):
    def __init__(self, id: int, task: str, done: bool = False) -> None:
        self.id = id
        self.task = task
        self.done = done

    def to_dict(self) -> dict:
        return {'id': self.id, 'task': self.task, 'done': self.done}


def deserialize_todo(t: dict) -> Todo:
    id: int
    task: str
    done: bool

    if not 'id' in t:
        raise AttributeError('no todo ID provided')
    else:
        id = int(t['id'])

    if not 'task' in t:
        raise AttributeError('no task provided')
    elif not isinstance(t['task'], str):
        raise TypeError('task must be a string')
    else:
        task = t['task']

    if not 'done' in t:
        done = False
    elif not isinstance(t['done'], bool):
        raise TypeError('done field must be a Boolean')

    return Todo(id=id, task=task, done=done)


class User(Jsonable):
    def __init__(self, id: int, name: str, todos: List[Todo] = []) -> None:
        self.id = id
        self.name = name
        self.todos = todos

    def __del__(self) -> None:
        if self.todos != []:
            self.todos = []

    def to_dict(self) -> dict:
        return {'id': self.id, 'name': self.name, 'todos': [todo.to_dict() for todo in self.todos]}


def deserialize_user(u: dict) -> Todo:
    id: int
    name: str
    todos: List[Todo]

    if not 'id' in u:
        raise AttributeError('no user ID provided')
    else:
        id = int(u['id'])

    if not 'name' in u:
        raise AttributeError('no user name provided')
    elif not isinstance(u['name'], str):
        raise TypeError('user name must be a string')
    else:
        name = u['name']

    if not 'todos' in u:
        todos = []
    elif not isinstance(u['todos'], list):
        raise TypeError('user todos must be an array')
    else:
        todos = [deserialize_todo(todo) for todo in u['todos']]

    return User(id=id, name=name, todos=todos)


USERS: List[User] = []


def response_with_location_header(user_id: int) -> Response:
    res = Response(status=202)
    location = f'/users/{user_id}'
    res.headers['Location'] = location
    return res


def create_user(user: User) -> None:
    for u in USERS:
        if u.id == user.id:
            raise AttributeError(f'a user with ID {u.id} already exists')

    USERS.append(user)


def get_user(user_id: int) -> User:
    users = list(filter(lambda u: u.id == user_id, USERS))

    if len(users) == 0:
        return None
    elif len(users) > 1:
        raise AttributeError(f'multiple users with the ID {user_id}')
    else:
        return users[0]


@app.route('/users', methods=('GET', 'POST'))
def users_endpoint() -> Response:
    if request.method == 'GET':
        return jsonify([user.to_dict() for user in USERS])
    elif request.method == 'POST':
        if request.is_json:
            content = request.get_json()

            try:
                new_user = deserialize_user(content)

                try:
                    create_user(new_user)
                    return response_with_location_header(new_user.id)
                except AttributeError as e:
                    return Response(status=409, response=str(e))

            except (AttributeError, TypeError) as e:
                return Response(status=400, response=str(e))
        else:
            return Response(status=405, response='no JSON supplied')


@app.route('/users/<int:user_id>', methods=('GET', 'DELETE'))
def user_by_id(user_id: int) -> Response:
    try:
        user = get_user(user_id)

        if user is None:
            return Response(status=404)
        else:
            if request.method == 'GET':
                return jsonify(user.to_dict())
            elif request.method == 'DELETE':
                USERS.remove(user)
                return Response(status=200)

    except AttributeError as e:
        return Response(status=409, response=str(e))


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    app.run()


if __name__ == '__main__':
    main()
