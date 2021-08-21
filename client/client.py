import logging
import os
import random
import time

from pythonjsonlogger import jsonlogger
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(jsonlogger.JsonFormatter())
logger.addHandler(logHandler)


def coin_flip() -> bool:
    return bool(random.getrandbits(1))


def main():
    http_endpoint = f"http://{os.environ['API_HOST']}:{os.environ['API_PORT']}"
    whattime_endpoint = f'{http_endpoint}/whattimeisitrightnow'

    logger.info('connecting to API', extra={'address': http_endpoint})

    s = requests.Session()
    retries = Retry(total=20, backoff_factor=0.5)

    s.mount('http://', HTTPAdapter(max_retries=retries))

    while True:
        time_format = random.choice(['raw', 'formatted'])
        params = {'format': time_format}

        res = s.get(whattime_endpoint, params=params)
        logger.info('response received', extra={
                    'status': res.status_code, 'endpoint': whattime_endpoint})


if __name__ == '__main__':
    main()
