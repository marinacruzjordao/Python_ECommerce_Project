from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re

# Create your models here.
class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    birth_date = models.DateField()
    nif = models.CharField(max_length=11)
    address = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=8)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user}'

    #to validate parameters
    def clean(self):
        error_messages = {}

        if len(self.zip_code)<8:
            error_messages['zip_code'] = 'Invalid zip code, only 8 characters'
        
        if error_messages:
            raise ValidationError(error_messages)
            