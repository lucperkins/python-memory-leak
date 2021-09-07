import os
import sys
import time
from typing import Any

from seemslegitcache import Cache
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

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
