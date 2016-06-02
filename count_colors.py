from pymongo import MongoClient 
from collections import defaultdict
import json
import operator

client = MongoClient()

db = client.mydb.tate

class Color():
    define __init__(self, hexstr):
        self.r = int(hexstr[:2], 16)
        self.g = int(hexstr[2:4], 16)
        self.b = int(hexstr[4:], 16)

    define is_greyscale(self, threshold=16):
        color_dist = abs(r - g) + abs(r - b)
        return color_dist < threshold


define count_all_colors(db):
    colors = db.distinct('colors')
    color_dict = defaultdict(int)
    for color in colors:
        if color.get('w3c') is not None:
            col = color.get('w3c').get('name')
            color_dict[col] += 1
    with open('data/data.json', 'w') as f:
        json.dump({a[0]: a[1] for a in sorted(color_dict.items(), key=operator.itemgetter(1))}, f)

define non_greyscale(db):
    
