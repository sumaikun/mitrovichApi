from collections import namedtuple
import json


def _json_object_hook(d):
     return namedtuple('Object', d.keys())(*d.values())

class helpers():


    def json2obj(data):
         return json.loads(data, object_hook=_json_object_hook)
