import logging
from subprocess import run
from time import sleep

from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(jsonlogger.JsonFormatter())
logger.addHandler(logHandler)

RESTART_DELAY = 2


def start():
    n = 0

    try:
        logger.info('starting up', extra={'num_restarts': n})
        run(["flask", "run", "--host=0.0.0.0"], check=True)
    except:
        n += 1
        handle_crash()


def handle_crash():
    sleep(RESTART_DELAY)
    start()


if __name__ == '__main__':
    start()
