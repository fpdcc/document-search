from django.core.exceptions import ValidationError

def validate_positive_int(value):
    if int(value) <= 0:
        raise ValidationError(
            ("Please enter a positive number, %(value)s is not valid."),
            params={"value": value},
        )
    
def validate_range(min, max):
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


def check_value(value):
    # For testing purposes only. Delete before finishing
    if value:
        print("The value is:", value)