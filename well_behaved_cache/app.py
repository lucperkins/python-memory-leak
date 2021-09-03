import os
import sys
import time
from typing import Any

from expiringdict import ExpiringDict
from flask import Flask, jsonify, request, Response

app = Flask(__name__)


class Cache(object):
    def __init__(self) -> None:
        self.stagger = int(os.environ['STAGGER'])

        max_items = int(os.environ['CACHE_MAX_ITEMS'])
        max_age = int(os.environ['CACHE_MAX_AGE_SECS'])
        self.cache = ExpiringDict(max_len=max_items, max_age_seconds=max_age)

    def stagger(self) -> None:
        time.sleep(self.stagger)

    def get(self, key: str) -> Any:
        self.stagger()
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        self.stagger()
        self.cache[key] = value

    def info(self) -> dict:
        return {
            'num_cache_items': len(self.cache),
            'total_cache_size': sys.getsizeof(self.cache)
        }


CACHE = Cache()


@app.route('/cache/<string:key>', methods=('GET', 'PUT'))
def caching_endpoint(key: str):
    if request.method == 'GET':
        value = CACHE.get(key)

        if value is None:
            return Response(status=404)
        else:
            return jsonify({'value': value})
    elif request.method == 'PUT':
        content = request.json

        if content is None:
            return Response(status=400, response='payload must be JSON')
        else:
            value = content.get('value')

            if value is None:
                return Response(status=400, response='must supply a value field')
            else:
                CACHE.set(key, value)
                return Response(status=204)


@app.route('/info')
def info_endpoint():
    return jsonify(CACHE.info())


if __name__ == '__main__':
    sys.setswitchinterval(sys.maxsize)

    app.run()
