from django.core.exceptions import ValidationError
import re

def validate_positive_int(value):
    # Check that the value is a positive integer

    if not value.isnumeric() or int(value) <= 0:
        raise ValidationError(
            ("Please enter a positive number, '%(value)s' is not valid."),
            params={"value": value},
        )


def validate_int_range(min, max):
    # Check that a 2 integer range is between the min and max

    def validator(value):
        # Change the NumericRange obj to an indexable array of ints
        value_list = value.__str__().strip('][').split(', ')
        if value_list[1] == 'None':
            raise ValidationError("Please enter values into both fields")
        value_list = [int(num) for num in value_list]
        
        if value_list[0] < min or value_list[1] > max:
            raise ValidationError(
                ("Please enter a valid range between %(min)s and %(max)s. Range %(value0)s and %(value1)s is not valid."),
                params={
                    "value0": value_list[0],
                    "value1": value_list[1],
                    "min": min,
                    "max": max
                },
            )

    return validator


def validate_int_btwn(min, max):
    # Check that a single integer is between the min and max

    def validator(value):
        if int(value) < min or int(value) > max:
            raise ValidationError(
                ("Please enter a number between %(min)s and %(max)s. The number %(value)s is not valid."),
                params={
                    "value": value,
                    "min": min,
                    "max": max
                },
            )
    
    return validator


def validate_int_array(min, max):
    # Check that a list/array of integers is between the min and max

    def validator(value):
        valid = True
        invalid_ints = []

        for int in value:
            if int < min or int > max:
                valid = False
                invalid_ints.append(int)
        
        if not valid:
            invalid_ints = [str(i) for i in invalid_ints]
            raise ValidationError(
                ("Please enter numbers between %(min)s and %(max)s. The number(s) %(invalid)s is/are not valid."),
                params={
                    "invalid": ", ".join(invalid_ints),
                    "min": min,
                    "max": max
                },
            )

    return validator


def validate_date(value):
    pattern = re.compile(r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$")
    date_error='Please enter the date as "YYYY-MM-DD", ensuring that the date exists. The date %(value)s is not valid.'

    if not re.fullmatch(pattern, value):
        raise ValidationError(
                (date_error),
                params={"value": value,},
            )
    year = int(value[0:4])
    month = int(value[5:7])
    day = int(value[8:])

    # Validate days for most months
    if month in [4,6,9,11] and day > 30:
        raise ValidationError(
                (date_error),
                params={"value": value,},
            )
    elif month in [1,3,5,7,8,10,12] and day > 31:
        raise ValidationError(
                (date_error),
                params={"value": value,},
            )

    # Account for February
    if year % 4 == 0 and month == 2 and day > 29:
        raise ValidationError(
                (date_error),
                params={"value": value,},
            )
    elif year % 4 != 0 and month == 2 and day > 28:
        raise ValidationError(
                (date_error),
                params={"value": value,},
            )


def check_value(value):
    # TODO: For testing purposes only. Delete before finishing
    if value:
        print("The value is:", value)