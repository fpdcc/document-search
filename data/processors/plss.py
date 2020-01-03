import re


def format_array(val):
    """
    Format a Python list to write it to CSV and import it as a PG ArrayField.
    """
    if val:
        if type(val) is str:
            return '{' + str(int(val)) + '}'
        else:
            lst = [int(v) for v in val]
            return str(lst).replace('[', '{').replace(']', '}')
    else:
        return "{}"


def check(row, geotype, geoname):
    if geotype and geotype != row[geoname]:
        raise ValueError(
            f'{geoname.title()}s do not match for {row["source_file"]}: {geotype}, {row[geoname]}'
        )


def check_plss(row, section=None, township=None):
    """
    Given a PLSS code, confirm that the section and township as recorded
    in the data are correct.
    """
    for geotype, geoname in ((section, 'section'), (township, 'township')):
        check(row, geotype, geoname)


def get_plss_codes(row, plss_field, check_codes=False):
    # Attempt to parse section, township, and range from location
    if row[plss_field]:
        # If there is a map_number and a location, it's a particular
        # error in the data where map_number is the range and location
        # is the map_number
        if row.get('map number'):
            townships, sections = row['township'], row['section']
            ranges = row['map number']
            row['map number'] = row[plss_field]
            row[plss_field] = None
        # There are four different formats that we expect for location:
        # 1. section-township-range
        elif re.findall(r'^\d{1,2}-\d{1,2}-\d{1,2}$', row[plss_field]):
            sections, townships, ranges = row[plss_field].split('-')
            if check_codes:
                check_plss(row, sections, townships)
        # 2. section,section-township-range
        elif re.findall(r'^(?:\d{1,2},){1,}\d{1,2}-\d{1,2}-\d{1,2}$', row[plss_field]):
            geogs = row[plss_field].split(',')
            sections, plss_code = geogs[:-1], geogs[-1]
            section, township, range_ = plss_code.split('-')
            sections += [section]
            townships, ranges = township, range_
        # 3. section,section-township-range,range
        elif re.findall(r'^(?:\d{1,2},){1,}\d{1,2}-\d{1,2}-\d{1,2},(?:\d{1,2},){0,}\d{1,2}$', row[plss_field]):
            plss_code = re.findall(r'\d{1,2}-\d{1,2}-\d{1,2}', row[plss_field])[0]
            section, township, range_ = plss_code.split('-')
            sections, ranges = row[plss_field].split(f',{plss_code},')
            sections = sections.split(',') + [section]
            ranges = ranges.split(',') + [range_]
            townships = township
        # 4. section-township-range,section-township-range
        elif re.findall(r'^(?:\d{1,2}-\d{1,2}-\d{1,2},){1,}\d{1,2}-\d{1,2}-\d{1,2}$', row[plss_field]):
            plss_codes = row[plss_field].split(',')
            sections = list(set([code.split('-')[0] for code in plss_codes]))
            townships = list(set([code.split('-')[1] for code in plss_codes]))
            ranges = list(set([code.split('-')[2] for code in plss_codes]))
        else:
            raise ValueError(
                f'Unexpected Location pattern: {row[plss_field]}'
            )
    else:
        sections, townships, ranges = row['section'], row['township'], None
    return sections, townships, ranges
