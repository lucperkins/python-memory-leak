import asyncio
import logging
import os
from random import choices
from string import printable
from typing import Any

from httpx import AsyncClient, AsyncHTTPTransport
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(jsonlogger.JsonFormatter())
logger.addHandler(logHandler)

HTTP_ENDPOINT = f"http://{os.environ['API_HOST']}:{os.environ['API_PORT']}"
PAYLOAD_SIZE = int(os.environ['PAYLOAD_SIZE'])


def log_result(key: str, method: str, status: int) -> None:
    logger.info('response received', extra={
        'key': key, 'method': method, 'status': status})


def random_text() -> str:
    return ''.join(choices(printable, k=PAYLOAD_SIZE))


async def main():
    logger.info('connecting to cache API',
                extra={'address': HTTP_ENDPOINT, 'payload_size': PAYLOAD_SIZE})
    cache_endpoint = f'{HTTP_ENDPOINT}/cache'

    transport = AsyncHTTPTransport(retries=20)

    async with AsyncClient(transport=transport) as client:
        n = 1

        while True:
            key = f"key-{n}"
            endpoint = f"{cache_endpoint}/{key}"
            res = await client.put(endpoint, json={'value': random_text()})
            log_result(key, 'PUT', res.status_code)
            n += 1


if __name__ == '__main__':
    asyncio.run(main())
