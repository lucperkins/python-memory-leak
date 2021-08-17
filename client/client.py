from random import randrange
import logging
import os
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class Client(object):
    def __init__(self, root_url: str) -> None:
        sesh = requests.Session()
        retries = Retry(total=10)
        sesh.mount('http://', HTTPAdapter(max_retries=retries))

        self.session = sesh
        self.users_endpoint = f'{root_url}/users'

    def create_user(self, user_id: int) -> None:
        user_dict = {
            'id': user_id,
            'name': 'someuser',
            'todos': [
                {
                    'id': 1,
                    'task': 'Get this example to work',
                    'done': False
                },
                {
                    'id': 2,
                    'task': 'Fix the broken example later',
                    'done': True
                }
            ]
        }

        res = self.session.post(self.users_endpoint, json=user_dict)
        print(res.status_code)

    def delete_user(self, user_id: int) -> None:
        user_endpoint = f'{self.users_endpoint}/{user_id}'

        res = self.session.delete(user_endpoint)
        print(res.status_code)


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

    while True:
        user_id = randrange(1000)
        client.create_user(user_id)
        time.sleep(0.01)
        client.delete_user(user_id)
        time.sleep(0.01)


if __name__ == '__main__':
    main()
