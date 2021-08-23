import logging
import os
from random import choices, getrandbits, randrange
from string import ascii_lowercase, ascii_uppercase, digits

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


def coin_flip() -> bool:
    return bool(getrandbits(1))


def log_result(endpoint: str, method: str, status: int) -> None:
    logger.info('response received', extra={
        'endpoint': endpoint, 'method': method, 'status': status})


def random_text() -> str:
    value_length = randrange(25, 100)
    return ''.join(choices(ascii_lowercase + ascii_uppercase + digits, k=value_length))


def main():
    http_endpoint = f"http://{os.environ['API_HOST']}:{os.environ['API_PORT']}"
    cache_endpoint = f'{http_endpoint}/cache'

    logger.info('connecting to cache API', extra={'address': http_endpoint})

    s = requests.Session()
    retries = Retry(total=20, backoff_factor=0.5)

    s.mount('http://', HTTPAdapter(max_retries=retries))

    n = 1

    while True:
        res: Response

        key = f'key-{n}'
        value = random_text()
        print(value)
        key_endpoint = f'{cache_endpoint}/{key}'

        # PUT to the cache
        res = s.post(key_endpoint, json={'value': value})
        log_result(key_endpoint, 'POST', res.status_code)

        # GET previously written keys from the cache 10 times (some will be missing)
        for _ in range(0, 10):
            r = randrange(0, n)
            random_key_endpoint = f'{cache_endpoint}/key-{r}'
            res = s.get(random_key_endpoint)
            log_result(random_key_endpoint, 'GET', res.status_code)

        n += 1


if __name__ == '__main__':
    main()
