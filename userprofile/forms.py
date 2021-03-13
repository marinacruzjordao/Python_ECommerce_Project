from django import forms
from django.contrib.auth.models import User
from . import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Userprofile
        fiedls = '__all__'
        exclude = ('user',)

class UserForm(forms.ModelForm):
    class Meta:
        model= User
        field = ('first_name','last_name','username','password','email')
    
    def clean(self):
        #method to validate
        data = self.data
        cleaned = self.cleaned_data

