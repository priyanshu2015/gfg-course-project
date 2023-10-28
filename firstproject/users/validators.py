from django.core.validators import RegexValidator


phone_number_regex = RegexValidator(
    regex="^[0-9]{10}$",
    message="phone_number must only contain numbers and should have a length of 10"
)