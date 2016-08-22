import psutil as ps
import os

import time
from datetime import datetime as dt
import ujson

LOGS = './logs/'
TIME = time.time()
FILENAME = '{}{}.json'.format(LOGS, dt.fromtimestamp(TIME).strftime('%Y-%m-%d %H-%M-%S'))
UPDATE_TIME = 10  # seconds


def dump(data):
    with open(FILENAME, mode='w') as file:
        ujson.dump(data, file)


def load(filename):
    with open(filename, mode='r') as file:
        raw = ujson.load(file)
        data = {int(timestamp): ps._common.snetio(*fields) for timestamp, fields in raw.items()}
    return data


if __name__ == '__main__':
    if not os.path.exists(LOGS):
        os.mkdir(LOGS)
    data = {}
    while True:
        data.update({int(time.time()): ps.net_io_counters()})
        dump(data)
        time.sleep(UPDATE_TIME)
