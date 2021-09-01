import json
from typing import Any


class Cache(object):
    def __init__(self) -> None:
        self.cache = {}

    def get(self, key: str) -> Any:
        return self.cache.get(key)

    def put(self, key: str, value: Any) -> None:
        self.cache[key] = value


CACHE = Cache()


def lambda_handler(event: dict, _context) -> dict:
    operation: str

    if 'operation' in event:
        operation = event['operation']
    else:
        return {
            'statusCode': 400,
            'body': {
                'error': 'No operation specified'
            }
        }

    if not 'key' in event:
        return {
            'statusCode': 400,
            'error': 'no cache key specified'
        }
    else:
        key = event['key']

        if operation == 'get':
            value = CACHE.get(key)

            if value is None:
                return {
                    'statusCode': 404,
                    'error': f'key {key} not present in cache'
                }
            else:
                return {
                    'statusCode': 200,
                    'body': value
                }
        elif operation == 'put':
            if not 'value' in event:
                return {
                    'statusCode': 400,
                    'error': f'no value specified'
                }
            else:
                value = event['value']
                CACHE.put(key, value)
                return {
                    'statusCode': 204
                }
        else:
            return {
                'statusCode': 400,
                'error': f'operation {operation} not recognized'
            }
