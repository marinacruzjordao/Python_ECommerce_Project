from django import http
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.db.models import Q

from pprint import pprint
from . import models
from userprofile.models import Userprofile


# Create your views here.
class ListProducts(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name= 'products'
    paginate_by=3
    ordering=['-id']

class Search(ListProducts):
    def get_queryset(self, *args, **kwargs):
        term = self.request.GET.get('term') or self.request.session['term']
        qs= super().get_queryset(*args, **kwargs)

        if not term:
            return qs

        self.request.session['term'] =term

        qs=qs.filter(
            Q(name__icontains=term) |
            Q(description_short__icontains=term) |
            Q(description_long__icontains=term) 
        )

        self.request.session.save()

        return qs
    

class DetailProduct(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name= 'product' 
    slug_url_kwarg = 'slug'

class AddToCart(View):
    def get(self, *args, **kwargs):
#        if self.request.session.get('cart'):
#            del self.request.session['cart']
#            self.request.session.save()

        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:lists')
        )

        variance_id = self.request.GET.get('vid') #string

        #validate if appear in the url
        if not variance_id:
            messages.error(
                self.request,
                'Product does not exist'
            )
            return redirect(http_referer)
        
        #obtain the object variation that user want to by
        variance = get_object_or_404(models.Variance, id = variance_id)
        variance_stock = variance.stock
        product = variance.product

        product_id = product.id
        product_name = product.name
        variance_name = variance.name or ''
        price_unit = variance.price
        price_unit_promotion = variance.price_promotion
        quantity = 1
        slug= product.slug
        image =  product.image

        if image:
            image =image.name
        else:
            image= ''

        #validate if there is stock
        if variance.stock <1 :
            messages.error(self.request,'stock out')
            return redirect(http_referer) #return to previous page

        # obtain key cart in session
        if not self.request.session.get('cart'):
            self.request.session['cart']={}
            self.request.session.save()
        
        cart = self.request.session['cart']
        
        #id variance exists in cart?
        if variance_id in cart:
            quantity_cart = cart[variance_id]['quantity']#obtain the actual quantity
            quantity_cart +=1

            if variance_stock< quantity_cart: 
                messages.warning(self.request, f'Stock out for {quantity_cart}x in product {product_name}. Add {variance_stock}X in your cart.')
                quantity_cart = variance_stock
            
            cart[variance_id]['quantity'] =  quantity_cart
            cart[variance_id]['price_quantity'] =  price_unit * quantity_cart
            cart[variance_id]['price_quantity_promotion'] =  price_unit_promotion * quantity_cart

        else:
            cart[variance_id] =  {
                'product_id' : product_id,
                'product_name': product_name,
                'variance_name' : variance_name, 
                'variance_id' : variance_id,
                'price_unit' : price_unit,
                'price_unit_promotion' : price_unit_promotion,
                'price_quantity': price_unit,
                'price_quantity_promotion': price_unit_promotion,
                'quantity' : 1,
                'slug' : slug,
                'image':  image,
            }

        self.request.session.save() # session save
        messages.success(self.request,f'Product {product_name} {variance_name} add to cart {cart[variance_id]["quantity"]}x')
        return redirect(http_referer)

class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        #check if cart session 

        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:lists')
        )

        variance_id = self.request.GET.get('vid')

        if not variance_id:
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            return redirect(http_referer)

        if variance_id not in self.request.session['cart']:
            return redirect(http_referer)

        cart = self.request.session['cart'][variance_id]

        messages.success(self.request,
        f'Product {cart["product_name"]} {cart["variance_name"]} was removed from cart.')
        
        del self.request.session['cart'][variance_id]
        self.request.session.save()

        return redirect(http_referer)

class Cart(View):
    def get(self, *args, **kwargs):
        cont = {
            'cart' : self.request.session.get('cart',{})
        }

        return render(self.request,'product/cart.html', cont)

class Finish(View):

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('userprofile:create')

        userprofile = Userprofile.objects.filter(user=self.request.user).exists() # verify if user exists
        if not userprofile:
            messages.error(self.request, 'User withou profile.')
            return redirect('userprofile:create')

        if not self.request.session.get('cart'):
           messages.error(self.request, 'Empty cart.')
           return redirect('product:lists')
            

        cont={
            'user': self.request.user,
            'cart': self.request.session['cart'],
        }
        return render(self.request,'product/finish.html', cont)