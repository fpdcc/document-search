import sys
import csv
import re

if __name__ == '__main__':
    extract_field = sys.argv[1]
    reader = csv.DictReader(sys.stdin)
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames + ['description'])
    writer.writeheader()
    for row in reader:
        # We expect IDs in the following formats:
        #   * 1234
        #   * 1234A
        #   * O-1234
        #   * A - 1234
        if re.findall(r'(?:^\d{1,}$|^\d{1,}[A-Z]$|^O-\d{1,}$|^A - \d{1,}$)', row[extract_field]):
            row['description'] = None
        else:
            # Field is a description; extract it out
            row['description'] = row[extract_field]
            row[extract_field] = None
        writer.writerow(row)
