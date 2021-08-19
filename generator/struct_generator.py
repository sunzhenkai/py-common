# coding: utf-8
from utils.generator.base_data_generator import generate_base_data


TYPE_STRING = {
    'type': str
}


def generate_struct(struct_def: dict) -> dict:
    res = {}
    for k, config in struct_def.items():
        res[k] = generate_base_data(config)
    return res


if __name__ == '__main__':
    c = {
        'id': TYPE_STRING,
    }
    record = generate_struct(c)
    print(record)
