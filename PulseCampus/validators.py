from django.core.exceptions import ValidationError
from datetime import date

def id_validate(x):
    if len(x) != 6 or not x.isdigit():
        raise ValidationError('Enter your valid Student ID.')

def no_digit(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('Should not contain digits.')
    
def no_future_date(value):
    if value > date.today():
        raise ValidationError('Date cannot be in the future.')
    
# def contact_validator(x):
#     if not x.isdigit() or len(x)<11:
#         raise ValidationError("Enter a valid Contact Number")
    
def all_digits(value):
    if not value.isdigit():
        raise ValidationError("Must be all digits")
   
def file_less_than_2mb(value):
    limit = 2 * 1024 * 1024  
    if value.size > limit:
        raise ValidationError("The maximum file size that can be uploaded is 2MB")