from django.core.validators import RegexValidator


phone_number_regex = RegexValidator(
    regex="^[\d]+$",
    message="phone_number must only contain numbers",
)