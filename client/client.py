import logging
import os
from random import choices, randrange
from string import printable
from typing import Any

from pythonjsonlogger import jsonlogger
import requests
from requests import Response
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(jsonlogger.JsonFormatter())
logger.addHandler(logHandler)


def log_result(endpoint: str, method: str, status: int) -> None:
    logger.info('response received', extra={
        'endpoint': endpoint, 'method': method, 'status': status})


def random_text() -> str:
    value_length = randrange(750, 1000)
    return ''.join(choices(printable, k=value_length))


class Client(object):
    def __init__(self) -> None:
        http_endpoint = f"http://{os.environ['API_HOST']}:{os.environ['API_PORT']}"
        logger.info('connecting to cache API',
                    extra={'address': http_endpoint})

        cache_endpoint = f'{http_endpoint}/cache'

        self.endpoint = cache_endpoint

        s = requests.Session()
        retries = Retry(total=20, backoff_factor=0.5)
        s.mount('http://', HTTPAdapter(max_retries=retries))
        self.session = s

    def get(self, key: str) -> None:
        key_endpoint = f'{self.endpoint}/{key}'
        res = self.session.get(key_endpoint)
        log_result(key_endpoint, 'GET', res.status_code)

    def put(self, key: str, value: Any) -> None:
        key_endpoint = f'{self.endpoint}/{key}'
        res = self.session.put(key_endpoint, json={'value': value})
        log_result(key_endpoint, 'PUT', res.status_code)


def main():
    client = Client()
    n = 1

    while True:
        # PUT to the cache
        client.put("key-{n}", random_text())
        n += 1


if __name__ == '__main__':
    main()
