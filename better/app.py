from typing import List, Type
import logging

from flask import Flask, jsonify, request, Response

app = Flask(__name__)


class Jsonable(object):
    def serialize(self) -> dict:
        pass


class JsonableList(object):
    def serialize(self) -> List[dict]:
        pass


class Todo(Jsonable):
    def __init__(self, id: int, task: str, done: bool = False) -> None:
        self.id = id
        self.task = task
        self.done = done

    def serialize(self) -> dict:
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
    else:
        done = bool(t['done'])

    return Todo(id=id, task=task, done=done)


class User(Jsonable):
    def __init__(self, id: int, name: str, todos: List[Todo] = []) -> None:
        self.id = id
        self.name = name
        self.todos = todos

    def serialize(self) -> dict:
        return {'id': self.id, 'name': self.name, 'todos': [todo.serialize() for todo in self.todos]}


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


class Users(JsonableList):
    def __init__(self, users: List[User] = []) -> None:
        self.users = users

    def add_user(self, user: User) -> None:
        for u in self.users:
            if u.id == user.id:
                raise AttributeError(f'a user with ID {u.id} already exists')

        self.users.append(user)

    def get_user(self, user_id: int) -> User:
        users_by_id = list(filter(lambda u: u.id == user_id, self.users))

        if len(users_by_id) == 0:
            return None
        elif len(users_by_id) > 1:
            raise AttributeError(f'multiple users with the ID {user_id}')
        else:
            return users_by_id[0]

    def delete_user(self, user_id: int) -> None:
        for idx, u in enumerate(self.users):
            if u.id == user_id:
                del self.users[idx]

    def add_todo_to_user(self, user_id: int, todo: Todo) -> None:
        for idx, u in enumerate(self.users):
            if u.id == user_id:
                self.users[idx].todos.append(todo)

    def serialize(self) -> List[dict]:
        return [user.serialize() for user in self.users]


USERS: Users = Users()


@app.route('/users', methods=('GET', 'POST'))
def users_endpoint() -> Response:
    if request.method == 'GET':
        return jsonify(USERS.serialize())
    elif request.method == 'POST':
        if request.is_json:
            content = request.get_json()

            try:
                new_user = deserialize_user(content)

                try:
                    USERS.add_user(new_user)
                    res = Response(status=202)
                    location = f'/users/{new_user.id}'
                    res.headers['Location'] = location
                    return res

                except AttributeError as e:
                    return Response(status=409, response=str(e))

            except (AttributeError, TypeError) as e:
                return Response(status=400, response=str(e))
        else:
            return Response(status=405, response='no JSON supplied')


@app.route('/users/<int:user_id>', methods=('GET', 'DELETE'))
def user_by_id(user_id: int) -> Response:
    try:
        user = USERS.get_user(user_id)

        if user is None:
            return Response(status=404)
        else:
            if request.method == 'GET':
                return jsonify(user.serialize())
            elif request.method == 'DELETE':
                USERS.delete_user(user.id)
                return Response(status=200)

    except AttributeError as e:
        return Response(status=409, response=str(e))


@app.route('/users/<int:user_id>/todos', methods=('GET', 'POST'))
def user_todos_by_id(user_id: int) -> Response:
    try:
        user = USERS.get_user(user_id)

        if user is None:
            return Response(status=404)
        else:
            if request.method == 'GET':
                return jsonify([todo.serialize() for todo in user.todos])
            elif request.method == 'POST':
                if request.is_json:
                    content = request.get_json()

                    try:
                        new_todo = deserialize_todo(content)

                        try:
                            USERS.add_todo_to_user(user.id, new_todo)

                            res = Response(status=202)
                            location = f'/users/{user.id}/todos/{new_todo.id}'
                            res.headers['Location'] = location
                            return res
                        except AttributeError as e:
                            return Response(status=409, response=str(e))

                    except (AttributeError, TypeError) as e:
                        return Response(status=400, response=str(e))
                else:
                    return Response(status=405, response='no JSON supplied')
    except AttributeError as e:
        return Response(status=409, response=str(e))


@app.route('/users/<int:user_id>/todos/<int:todo_id>', methods=('GET', 'DELETE'))
def todo_by_user_and_todo_id(user_id: int, todo_id: int) -> Response:
    try:
        user = USERS.get_user(user_id)

        if user is None:
            return Response(status=404)
        else:
            todos_by_id = list(
                filter(lambda t: t.id == todo_id, user.todos))

            if len(todos_by_id) == 0:
                return Response(status=404)
            elif len(todos_by_id) > 1:
                return Response(status=409, response=f'Multiple user todos with the ID {todo_id}')
            else:
                if request.method == 'GET':
                    return jsonify(todos_by_id[0].serialize())
                elif request.method == 'DELETE':
                    for idx, todo in enumerate(user.todos):
                        if todo.id == todo_id:
                            del user.todos[idx]
                    return Response(status=200)

    except AttributeError as e:
        return Response(status=409, response=str(e))


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    app.run()


if __name__ == '__main__':
    main()
