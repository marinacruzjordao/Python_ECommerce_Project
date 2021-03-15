from django.contrib.auth.models import User
from django.contrib.messages.api import error
from django.shortcuts import render,redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse, request
from django.contrib import messages

from product.models import Product, Variance
from .models import Request, ItemRequest

from utils import utils

# Create your views here.


class DispatchLoginRequiredMixin(View): # find the page should go
    def dispatch(self,  *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('userprofile:create')

        return super().dispatch( *args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):  #only user request can be seen by the user, is not able to see other users requests
        qs= super().get_queryset(*args, **kwargs)
        qs=qs.filter(user=self.request.user)
        return qs
 

class SaveRequest(View):

    template_name= 'request/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You require to do login.')
            return redirect('userprofile:create')
        
        if not self.request.session.get('cart'):
            messages.error(self.request,'Empty cart.')
            return redirect('product:lists')

        #validata if there is enough stock in data base
        #Obtain the key of item
        cart = self.request.session.get('cart')
        cart_variance_ids = [v for v in cart]
        bd_variance = list(Variance.objects.select_related('product').filter(id__in=cart_variance_ids))

        for vars in bd_variance:
            vid = str(vars.id)
            stock = vars.stock
            qtd_cart =  cart[vid]['quantity']
            price_unt = cart[vid]['price_unit']
            price_unt_promo = cart[vid]['price_unit_promotion']

            error_msg_stock=''
            
            if stock < qtd_cart:
                cart[vid]['quantity'] = stock
                cart[vid]['price_quantity'] = stock * price_unt
                cart[vid]['price_quantity_promotion'] = stock * price_unt_promo
            
                error_msg_stock='Stock out for some itens in cart. We decrease these products quantity. Verify your cart products affect by.'
            if error_msg_stock:
                messages.error(self.request, error_msg_stock)
                
                self.request.session.save()
                return redirect('product:cart')

        qtd_total_cart = utils.cart_total_qtd(cart)
        value_total_cart = utils.cart_totals(cart)

        request = Request(user=self.request.user, total= value_total_cart, qtd_total=qtd_total_cart, status='C',)
        request.save()

        ItemRequest.objects.bulk_create(
            ItemRequest(
                request=request,
                product=v['product_name'],
                product_id=v['product_id'],
                variance=v['variance_name'],
                variance_id=v['variance_id'],
                price=v['price_quantity'],
                price_promotion=v['price_quantity_promotion'],
                quantity=v['quantity'],
                image=v['image'],
            ) for v in cart.values()
        )

        del self.request.session['cart']

        return redirect(reverse('request:pay', kwargs={'pk': request.pk} ))


class Pay(DispatchLoginRequiredMixin, DetailView):
    template_name =  'request/pay.html'
    model= Request
    pk_url_kwarg='pk'
    context_object_name='request'



class Detail(DispatchLoginRequiredMixin, DetailView):
    model = Request
    context_object_name= 'request'
    template_name = 'request/detail.html'
    pk_url_kwarg = 'pk'


class Lists(DispatchLoginRequiredMixin, ListView):
    model = Request
    context_object_name= 'requests'
    template_name = 'request/lists.html'
    paginate_by = 10 # number of request per page
    ordering = ['-id']



































