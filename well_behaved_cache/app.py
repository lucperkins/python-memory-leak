from typing import Any

from expiringdict import ExpiringDict
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

CACHE = ExpiringDict(max_len=1000, max_age_seconds=60)


def cache_get(key: str) -> Any:
    return CACHE.get(key)


def cache_set(key: str, value: Any) -> None:
    if (key, value) not in CACHE.items():
        CACHE.update({key: value})


@app.route('/cache/<string:key>', methods=('GET', 'POST'))
def caching_endpoint(key: str):
    if request.method == 'GET':
        value = cache_get(key)

        if value is None:
            return Response(status=404)
        else:
            return jsonify({'value': value})
    elif request.method == 'POST':
        content = request.json

        if content is None:
            return Response(status=400, response='payload must be JSON')
        else:
            value = content.get('value')

            if value is None:
                return Response(status=400, response='must supply a value field')
            else:
                cache_set(key, value)
                return Response(status=204)


if __name__ == '__main__':
    app.run()
