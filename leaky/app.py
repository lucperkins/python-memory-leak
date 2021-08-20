from flask import Flask, Response

from hello import hello

app = Flask(__name__)


@app.route('/')
def index():
    quote = hello()
    return Response(status=200, response=quote)


def main():
    app.run()


if __name__ == '__main__':
    main()
