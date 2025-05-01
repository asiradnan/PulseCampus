from django.core.exceptions import ValidationError
    
def id_validate(x):
    if len(x) != 6 or not x.isdigit():
        raise ValidationError('Enter your valid Student ID.')

def no_digit(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('Should not contain digits.')
    
def date_validator(value):
    if value > date.today():
        raise ValidationError('Date cannot be in the future.')
    
def contact_validator(x):
    if not x.isdigit() or len(x)<11:
        raise ValidationError("Enter a valid Contact Number")
    
def all_digits(value):
    if not value.is_digit():
        raise ValidationError("Must be all digits")
   