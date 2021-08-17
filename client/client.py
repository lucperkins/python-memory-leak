import logging
import os
import time

import requests


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
    users_endpoint = f'{todos_api_endpoint}/users'

    while True:
        res = requests.get(users_endpoint)
        print(res.status_code)

        time.sleep(0.1)


if __name__ == '__main__':
    main()
