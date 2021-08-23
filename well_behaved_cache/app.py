from typing import Any

from expiringdict import ExpiringDict
from flask import Flask, jsonify, request, Response

app = Flask(__name__)


class Cache(object):
    def __init__(self):
        self.cache = ExpiringDict(max_len=1000, max_age_seconds=60)

    def get(self, key: str) -> Any:
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        if not (key, value) in self.cache.items():
            self.cache[key] = value


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


if __name__ == '__main__':
    app.run()
