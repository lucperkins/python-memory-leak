import os
from flask import Flask, jsonify, request, Response

from whattime import current_timestamp_raw, current_timestamp_formatted

app = Flask(__name__)


@app.route('/whattimeisitrightnow')
def index():
    if request.args.get('format') == 'formatted':
        current_time = {'rightnow': {
            'formatted': current_timestamp_formatted()}}
        return jsonify(current_time)
    elif request.args.get('format') == 'raw':
        current_time = {'rightnow': {'raw': current_timestamp_raw()}}
        return jsonify(current_time)
    else:
        return Response(status=400, response='You must specify either raw or formatted as a request parameter')


if __name__ == '__main__':
    app.run()
