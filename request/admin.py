from django.contrib import admin
from . import models


class ItemRequestInline(admin.TabularInline):
    model = models.ItemRequest
    extra = 1 

class RequestAdmin(admin.ModelAdmin):
    inlines=[ItemRequestInline]

# Register your models here.
admin.site.register(models.Request, RequestAdmin)
admin.site.register(models.ItemRequest)