from flask import Flask, jsonify

from whattime import current

app = Flask(__name__)


@app.route('/whattimeisitrightnow')
def index():
    current_time = {'rightnow': current()}

    return jsonify(current_time)


def main():
    app.run()


if __name__ == '__main__':
    main()
