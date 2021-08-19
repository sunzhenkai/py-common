# coding: utf-8

import csv


def write(fp: str, data: list, struct: dict):
    with open(fp, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(struct.keys())
        writer.writerows(data)
