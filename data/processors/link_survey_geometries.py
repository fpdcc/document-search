import sys
import csv
import json

from plss import format_array

if __name__ == '__main__':
    geometry_file = sys.argv[1]
    with open(geometry_file) as fobj:
        feature_collection = json.load(fobj)
        features = feature_collection['features']

    attrs = [
        'type', 'entity', 'diameter', 'material', 'description',
        'end_date', 'status', 'agreement_type'
    ]

    reader = csv.DictReader(sys.stdin)
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames + attrs + [
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

            for geotype in ['township', 'range', 'section']:
                row[geotype] = format_array(
                    list(set([prop[geotype] for prop in properties if prop[geotype] is not None]))
                )

            row['geometry'] = json.dumps({
                'type': 'GeometryCollection',
                'geometries': geometries
            })

            for attr in attrs:
                attr_set = list(set([
                    prop[attr] for prop in properties
                    if prop[attr] is not None and prop[attr] != 'NULL'
                ]))
                if len(attr_set) > 0:
                    # Technically attributes can have multiple values like the PLSS
                    # values, but unlike PLSS values it doesn't actually make sense for
                    # Licenses to have multi-valued attributes. Because of this, just
                    # accept one attribute per row.
                    value = attr_set[-1]
                    if attr == 'diameter':
                        try:
                            value = int(value)
                        except ValueError:
                            continue
                    row[attr] = value
                else:
                    row[attr] = None
        else:
            row['township'] = row['range'] = row['section'] = '{}'
        writer.writerow(row)
