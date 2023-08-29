# coding: utf-8
import json
from typing import List


# 读取文件, 按行切分
def read_lines(fn: str) -> List[str]:
    result = []
    with open(fn, 'r') as f:
        line = f.readline()
        while line:
            result.append(line)
            line = f.readline()
    return result


def load_multiple_json(fn: str):
    result = []
    lines = read_lines(fn)
    for line in lines:
        result.append(json.loads(line))
    return result
