from django.contrib import admin
from django.db import models
from . import models

# to have produc variance
class VarianceInline(admin.TabularInline):
    model = models.Variance
    extra = 1
 
class ProductAdmin(admin.ModelAdmin):
    #to show these parameters in admin page
    list_display = ['name','description_short','get_price_format','get_price_promo_format']
    inlines = [VarianceInline]

# Register your models here.
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Variance)