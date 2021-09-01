import json
from typing import Any

# The core application logic


class Cache(object):
    def __init__(self) -> None:
        self.cache = {}

    def get(self, key: str) -> Any:
        return self.cache.get(key)

    def put(self, key: str, value: Any) -> None:
        self.cache[key] = value

    def delete(self, key: str) -> None:
        del self.cache[key]


CACHE = Cache()


def lambda_handler(event: dict, _context) -> dict:
    operation: str

    if not 'operation' in event and not 'key' in event:
        print(json.dumps({
            'errors': [
                'no operation specified',
                'no key specified'
            ]
        }))

    if 'operation' in event:
        operation = event['operation']
    else:
        err = 'no operation specified'

        print(json.dumps({'errors': [err]}))

        return {
            'statusCode': 400,
            'error': err
        }

    if not 'key' in event:
        err = 'no cache key specified'

        print(json.dumps({'errors': [err]}))

        return {
            'statusCode': 400,
            'error': err
        }
    else:
        key = event['key']

        if operation == 'get':
            value = CACHE.get(key)

            if value is None:
                err = f'key {key} not present in cache'

                print(json.dumps({'errors': [err]}))

                return {
                    'statusCode': 404,
                    'error': err
                }
            else:
                print(json.dumps({'success': {'op': 'get', 'key': key}}))

                return {
                    'statusCode': 200,
                    'body': value
                }
        elif operation == 'put':
            if not 'value' in event:
                err = 'no value specified'

                print(json.dumps({'errors': [err]}))

                return {
                    'statusCode': 400,
                    'error': err
                }
            else:
                value = event['value']
                CACHE.put(key, value)

                print(json.dumps({'success': {'op': 'put', 'key': key}}))

                return {
                    'statusCode': 204
                }
        elif operation == 'delete':
            CACHE.delete(key)

            print(json.dumps({'success': {'op': 'delete', 'key': key}}))

            return {
                'statusCode': 204
            }
        else:
            err = f'operation {operation} not recognized'

            print(json.dumps({'errors': [err]}))

            return {
                'statusCode': 400,
                'error': err
            }
