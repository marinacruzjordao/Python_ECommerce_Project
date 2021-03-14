from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import copy

from . import models
from . import forms 

# Create your views here.

class BaseProfile(View):
    template_name ='userprofile/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        self.userprofile = None

        if self.request.user.is_authenticated:
            self.userprofile = models.Userprofile.objects.filter(user=self.request.user).first()

            self.context = {
                'userform' : forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                    ),
                'profileform': forms.ProfileForm(data=self.request.POST or None, instance=self.userprofile),
            }
        else:
            self.context = {
                'userform' : forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None),
            }

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']

        if self.request.user.is_authenticated:
            self.template_name = 'userprofile/update.html'

        self.renderization = render(self.request, self.template_name, self.context)


    def get(self, *args, **kwargs):
        return self.renderization


#class Create(BaseProfile):
class Create(BaseProfile):
    def post(self, *args, **kwargs):
        #validate if forms are valid
        #if not self.userform.is_valid() or not self.profileform.is_valid():
        if not self.userform.is_valid():

            return self.renderization

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        #user already log
        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user.username)
            user.username = username

            if password:
                user.set_password(password)

            user.email=email
            user.first_name = first_name
            user.last_name = last_name
            user.save() 

            if not self.userprofile:
                self.userprofile.cleaned_data['user']=user
                userprofile = models.Userprofile(**self.profileform.cleaned_data)
                userprofile.save()
            else:
                userprofile = self.profileform.save(commit=False)
                userprofile.user =  user
                userprofile.save()

        else:
            user = self.userform.save(commit=False) # save but not in the data base
            user.set_password(password) # to encrypt password
            user.save()
            
            userprofile = self.profileform.save(commit=False)
            userprofile.user = user
            userprofile.save()

        if password:
            authentic = authenticate(self.request, username=user, password=password)
            if authentic:
                login(self.request, user=user)

        #save cart
        self.request.session['cart']= self.cart
        self.request.session.save()

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

