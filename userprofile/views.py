from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse

from . import models
from . import forms 

# Create your views here.

class BaseProfile(View):
    template_name ='userprofile/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.context = {
            'userform' : forms.UserForm(data=self.request.POST or None),
            'profileform': forms.ProfileForm(data=self.request.POST or None),
        }


        self.renderization = render(self.request, self.template_name, self.context)


    def get(self, *args, **kwargs):
        return self.renderization


class Create(BaseProfile):
    pass

class Update(View):
    pass

class Login(View):
    pass

class Logout(View):
    pass

