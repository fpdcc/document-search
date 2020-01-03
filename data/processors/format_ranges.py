import sys
import csv
import re


def format_range(val):
    """
    Format a value for importing as a Postgres range type.
    """
    if not val:
        return None
    else:
        if re.findall(r'^\d{1,}-\d{1,}$', val):
            bounds = [str(int(bound)) for bound in val.split('-')]
            return f'[{",".join(bounds)}]'
        else:
            try:
                int_val = int(val)
            except ValueError:
                raise ValueError(f'Could not cast value to range type: {val}')
            else:
                return f'[{int_val},{int_val}]'


if __name__ == '__main__':
    range_fields = sys.argv[1:]
    reader = csv.DictReader(sys.stdin)
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        for range_field in range_fields:
            row[range_field] = format_range(row[range_field])
        writer.writerow(row)
