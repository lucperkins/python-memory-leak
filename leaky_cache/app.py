import os
import sys
import time
from typing import Any

from flask import Flask, jsonify, request, Response

app = Flask(__name__)


# Use this to burn CPU artificially
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    else:
        return(fibonacci(n-1) + fibonacci(n-2))


def burn_cpu(max_time: int) -> None:
    start_time = time.time()

    n = 0

    while (time.time() - start_time) < max_time:
        _value = fibonacci(n)
        n += 1


class Cache(object):
    def __init__(self) -> None:
        self.stagger = int(os.environ['STAGGER_SECONDS'])
        self.cache = {}

    def get(self, key: str) -> Any:
        burn_cpu(self.stagger)
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        burn_cpu(self.stagger)
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
