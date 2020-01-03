#!/usr/bin/env python3
import sys
import csv

from plss import format_array, get_plss_codes


if __name__ == '__main__':
    reader = csv.DictReader(sys.stdin)
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        sections, townships, ranges = get_plss_codes(row, 'section')
        row['section'] = format_array(sections)
        row['township'] = townships
        row['range'] = ranges
        writer.writerow(row)
