from django.core.exceptions import ValidationError

def validate_positive_int(value):
    if int(value) <= 0:
        raise ValidationError(
            ("Please enter a positive number, %(value)s is not valid."),
            params={"value": value},
        )