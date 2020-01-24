import sys
import csv
import json

if __name__ == '__main__':
    geometry_file = sys.argv[1]
    with open(geometry_file) as fobj:
        feature_collection = json.load(fobj)
        features = feature_collection['features']

    reader = csv.DictReader(sys.stdin)
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames + ['geometry'])
    writer.writeheader()

    for row in reader:
        license_no = row['license number']
        matching_features = [
            feature['geometry'] for feature in features
            if feature['properties']['license_no'] == license_no
        ]
        if len(matching_features) > 0:
            row['geometry'] = json.dumps({
                'type': 'GeometryCollection',
                'geometries': matching_features
            })
        writer.writerow(row)
