from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from . import models

# Create your views here.
class ListProducts(ListView):
    model = models.Product
    template_name = 'product/list.html'

class DetailProduct(View):
    pass

class AddToCart(View):
    pass

class RemoveFromCart(View):
    pass

class Cart(View):
    pass

class Finish(View):
    pass