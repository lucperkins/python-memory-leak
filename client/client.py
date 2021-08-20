import logging
import os
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


def main():
    http_endpoint = f"http://{os.environ['API_HOST']}:{os.environ['API_PORT']}"

    logger.info('connecting to API', extra={'address': http_endpoint})

    s = requests.Session()
    retries = Retry(total=20, backoff_factor=0.5)
    s.mount('http://', HTTPAdapter(max_retries=retries))

    while True:
        res = s.get(http_endpoint)
        logger.info('response received from %s', http_endpoint,
                    extra={'status': res.status_code})

        time.sleep(1)


if __name__ == '__main__':
    main()
