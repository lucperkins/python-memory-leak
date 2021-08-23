import logging
from subprocess import run
from time import sleep

RESTART_DELAY = 2


def start():
    try:
        logging.info('Starting up Flask application...')
        run(["flask", "run", "--host=0.0.0.0"], check=True)
    except:
        handle_crash()


def handle_crash():
    sleep(RESTART_DELAY)
    start()


if __name__ == '__main__':
    start()
