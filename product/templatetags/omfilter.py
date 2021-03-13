from django.template import Library
from utils import utils

register = Library()

@register.filter
def format_prices(val):
    #to format the product price
    return utils.format_prices(val)

@register.filter
def cart_total_qtd(cart):
    return utils.cart_total_qtd(cart)

@register.filter
def cart_totals(cart):
    return utils.cart_totals(cart)
