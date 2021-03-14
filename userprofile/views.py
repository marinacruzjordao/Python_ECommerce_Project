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

        if self.request.user.is_authenticated:
            self.context = {
                'userform' : forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                    ),
                'profileform': forms.ProfileForm(data=self.request.POST or None),
            }
        else:
            self.context = {
                'userform' : forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None),
            }


        self.renderization = render(self.request, self.template_name, self.context)


    def get(self, *args, **kwargs):
        return self.renderization


#class Create(BaseProfile):
class Create(BaseProfile):
    def post(self, *args, **kwargs):
        return self.renderization


class Update(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Update')

class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')

class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')

