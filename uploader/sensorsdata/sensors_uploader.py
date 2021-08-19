# coding: utf-8

import csv

import sensorsanalytics

KEY_DISTINCT_ID = 'distinct_id'
KEY_ITEM_ID = 'item_id'
KEY_ITEM_TYPE = 'item_type'


class SensorsUploader:
    def __init__(self, host, project, peoples, items, count: tuple, struct, offset: tuple = (0, 0),
                 switch=(True, True)):
        self.host = f"http://{host}:8106/sa?project={project}"
        self.peoples = peoples
        self.items = items
        self.count = count
        self.offset = offset
        self.struct = struct
        self.switch = switch
        self.consumer = sensorsanalytics.BatchConsumer(self.host)
        self.sa = sensorsanalytics.SensorsAnalytics(self.consumer)

    def upload(self):
        if self.peoples and self.switch[0]:
            for prop in self.generator(self.peoples, self.struct[0], self.count[0], self.offset[0]):
                distinct = prop.pop(KEY_DISTINCT_ID)
                self.sa.profile_set(distinct, prop, is_login_id=True)
        if self.items and self.switch[1]:
            for prop in self.generator(self.items, self.struct[1], self.count[1], self.offset[1]):
                td = prop.pop(KEY_ITEM_ID)
                tp = prop.pop(KEY_ITEM_TYPE)
                self.sa.item_set(tp, td, prop)
        self.sa.flush()

    @classmethod
    def generator(cls, fp, struct, count, start=0):
        with open(fp, 'r') as f:
            record = 0
            data = csv.reader(f)

            header = next(data)
            for line in data:
                if record % 10000 == 0:
                    print(f"progress {int(record / count * 10000) / 100.0}%, record {record} of {count}")

                record += 1
                if record < start:
                    continue

                properties = {}
                for i in range(len(header)):
                    pn = header[i]
                    cfg = struct[pn]
                    tp = cfg['type']
                    if type(tp) is tuple:
                        def psf(v):
                            if len(v) > 0 and v[0] in "'" and v[-1] == "'":
                                return v[1:-1]
                            return v

                        dl = line[i].strip()[1:-1].split(',')
                        properties[header[i]] = [cls.parse(tp[1] if 'prefix' not in cfg else str,
                                                           psf(j.strip())) for j in dl]
                    else:
                        # 有 prefix 配置的字段，最终类型为 str
                        properties[header[i]] = cls.parse(tp if 'prefix' not in cfg else str, line[i])
                yield properties

    @classmethod
    def parse(cls, tp, v):
        if tp is bool:
            if type(v) is str:
                return v == 'True'
            return bool(v)
        elif tp in [int, float, bool]:
            return tp(v)
        return v

    def close(self):
        self.sa.close()
