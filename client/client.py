import logging
import os
from random import choice, randrange
import time
from typing import List

from faker import Factory
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class Client(object):
    def __init__(self, root_url: str) -> None:
        sesh = requests.Session()
        retries = Retry(total=100, backoff_factor=0.5)
        sesh.mount('http://', HTTPAdapter(max_retries=retries))

        self.session = sesh
        self.users_endpoint = f'{root_url}/users'

    def create_user(self, user_id: int, name: str) -> None:
        user_dict = {
            'id': user_id,
            'name': name,
        }

        self.session.post(self.users_endpoint, json=user_dict)

    def delete_user(self, user_id: int) -> None:
        user_endpoint = f'{self.users_endpoint}/{user_id}'

        self.session.delete(user_endpoint)

    def add_todo_to_user(self, user_id: int, todo_id: int, todo_task: str) -> None:
        user_todos_endpoint = f'{self.users_endpoint}/{user_id}/todos'

        todo = {'id': todo_id, 'task': todo_task}
        self.session.post(user_todos_endpoint, json=todo)

    def delete_todo_from_user(self, user_id: int, todo_id: int) -> None:
        todo_endpoint = f'{self.users_endpoint}/{user_id}/todos/{todo_id}'
        self.session.delete(todo_endpoint)


def get_api_endpoint() -> str:
    api_host: str = os.environ.get('API_HOST')
    api_port: str = os.environ.get('API_PORT')

    if api_host is None or api_port is None:
        logging.error(
            'You must specify an API host and port via API_HOST and API_PORT')
        exit(1)

    return f'http://{api_host}:{api_port}'


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    todos_api_endpoint = get_api_endpoint()

    client = Client(root_url=todos_api_endpoint)

    user_ids = [*range(1, 1000)]
    names = ['jake_the_snake', 'adalovelace123',
             'timthetoolmantaylor', 'alborland420']
    tasks = ['pick up the dry cleaning', 'get off the couch for once',
             'be nicer to other people', 'get better at Python', 'keep reading the Datadog docs']

    fake = Factory.create()

    for user_id in user_ids:
        client.create_user(user_id=user_id, name=choice(names))

    # Do stuff
    while True:
        # Select a user
        user_id = randrange(1, 1000)

        # Create or delete the user
        if fake.boolean(chance_of_getting_true=50):
            client.create_user(user_id=user_id, name=choice(names))
        else:
            client.delete_user(user_id=user_id)

        # Add and delete todos (good mix of successful and unsuccessful operations)
        for todo_id in [*range(1, 10)]:
            if fake.boolean(chance_of_getting_true=50):
                client.add_todo_to_user(
                    user_id=user_id, todo_id=todo_id, todo_task=choice(tasks))
            else:
                client.delete_todo_from_user(user_id=user_id, todo_id=todo_id)

        time.sleep(0.1)


if __name__ == '__main__':
    main()
