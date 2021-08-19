# coding: utf-8
import random
import uuid
from datetime import datetime, timedelta

KEY_CANDIDATE = 'candidate'
KEY_MIN = 'min'
KEY_MAX = 'max'
KEY_SIZE = 'size'
KEY_TYPE = 'type'
KEY_PREFIX = 'prefix'
KEY_UNIQUE = 'unique'
KEY_VALUE = 'value'

DEFAULT_MIN_INT = 1
DEFAULT_MAX_INT = 1 << 31


def random_int(config: dict):
    return random.randint(config[KEY_MIN] if KEY_MIN in config else DEFAULT_MIN_INT,
                          config[KEY_MAX] if KEY_MAX in config else DEFAULT_MAX_INT)


def generate_base_data(config: dict):
    tp = config[KEY_TYPE]

    #
    # 先处理复杂类型
    #

    if type(tp) is tuple:
        cfg = tp
        if cfg[0] is list:
            assert KEY_SIZE in config
            sc = config[KEY_SIZE]
            size = sc if type(sc) is int else random.randint(sc[0], sc[1])
            if KEY_MAX in config or KEY_MIN in config:
                mi = config[KEY_MIN] if KEY_MIN in config else DEFAULT_MIN_INT
                ma = config[KEY_MAX] if KEY_MAX in config else DEFAULT_MAX_INT
                assert (ma - mi) > 2 * size, f"取值范围过小 [config={config}]"
            unique = config.get(KEY_UNIQUE)
            res = []
            us = set()
            while len(res) < size:
                g = generate_base_data({
                    **config,
                    'type': cfg[1]
                })
                if unique and g in us:
                    continue
                us.add(g)
                res.append(g)
            return list(res)

    #
    # 处理基本类型
    #

    # 如果指定候选集，则从候选集随机选
    res = None
    if KEY_VALUE in config:
        res = config[KEY_VALUE]
    elif KEY_CANDIDATE in config:
        res = random.choice(config[KEY_CANDIDATE])
    elif tp is int:
        res = random_int(config)
    elif tp is str:
        res = str(uuid.uuid4())
    elif tp is float:
        res = random_int(config) + 1e-5 * random.randint(1, 1000000)
    elif tp is datetime:
        start = config[KEY_MIN] if KEY_MIN in config else datetime.now() - timedelta(days=3)
        end = config[KEY_MAX] if KEY_MAX in config else datetime.now()
        res = random.randint(int(start.timestamp() * 1000), int(end.timestamp() * 1000))

    if KEY_PREFIX in config:
        res = str(config[KEY_PREFIX]) + str(res)
    return res


if __name__ == '__main__':
    c = [
        {
            'type': int,
            'max': 100,
            'prefix': 'ii'
        },
        {
            'type': str
        },
        {
            'type': (list, int),
            'min': 1,
            'max': 1000,
            'size': 10
        },
        {
            'type': (list, int),
            'min': 1,
            'max': 150,
            'size': 10,
            'unique': True
        },
        {
            'type': (list, str),
            'candidate': ['a', 'b', 'c', 'd'],
            'size': 10,
            'prefix': 'ii'
        },
        {
            'type': datetime
        },
        {
            'type': datetime,
            'min': datetime.now() - timedelta(days=10),
            'max': datetime.now() - timedelta(days=5)
        }
    ]
    for cf in c:
        data = generate_base_data(cf)
        print(data)
