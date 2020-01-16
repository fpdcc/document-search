import sys
import json

area_to_plss = {
    1: (42, 9),
    2: (42, 10),
    3: (42, 11),
    4: (42, 12),
    5: (42, 13),
    6: (41, 9),
    7: (41, 10),
    8: (41, 11),
    9: (41, 12),
    10: (41, 13),
    11: (41, 14),
    12: (40, 12),
    13: (40, 13),
    14: (40, 14),
    15: (39, 12),
    16: (39, 13),
    17: (39, 14),
    18: (38, 12),
    19: (38, 13),
    20: (38, 14),
    21: (38, 15),
    22: (37, 11),
    23: (37, 12),
    24: (37, 13),
    25: (37, 14),
    26: (37, 15),
    27: (36, 12),
    28: (36, 13),
    29: (36, 14),
    30: (36, 15),
    31: (35, 13),
    32: (35, 14),
    33: (35, 15)
}

plss_to_area = {plss: area for area, plss in area_to_plss.items()}

if __name__ == '__main__':
    geojson = json.load(sys.stdin)
    for feature in geojson['features']:
        properties = feature['properties']
        township, range_ = properties['township'], properties['range']
        try:
            feature['properties']['area'] = plss_to_area[(township, range_)]
        except KeyError:
            raise KeyError(
                f'No area found for township {township} and range {range_}'
            )
    json.dump(geojson, sys.stdout)
