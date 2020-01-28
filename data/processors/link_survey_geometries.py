import sys
import csv
import json

from plss import format_array

if __name__ == '__main__':
    geometry_file = sys.argv[1]
    with open(geometry_file) as fobj:
        feature_collection = json.load(fobj)
        features = feature_collection['features']

    reader = csv.DictReader(sys.stdin)
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames + [
        'geometry', 'township', 'range', 'section'
    ])
    writer.writeheader()

    for row in reader:
        license_no = row['license number']
        matching_features = [
            feature for feature in features
            if feature['properties']['license_no'] == license_no
        ]
        if len(matching_features) > 0:
            geometries = [feature['geometry'] for feature in matching_features]
            properties = [feature['properties'] for feature in matching_features]

            row['township'] = format_array(
                list(set([prop['township'] for prop in properties if prop['township'] is not None]))
            )
            row['range'] = format_array(
                list(set([prop['range'] for prop in properties if prop['range'] is not None]))
            )
            row['section'] = format_array(
                list(set([prop['section'] for prop in properties if prop['section'] is not None]))
            )

            row['geometry'] = json.dumps({
                'type': 'GeometryCollection',
                'geometries': geometries
            })
        else:
            row['township'] = row['range'] = row['section'] = '{}'
        writer.writerow(row)
