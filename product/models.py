from typing import Optional
from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):

    name = models.CharField(max_length=255)
    description_long = models.TextField()   
    description_short = models.TextField(max_length=255)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    price_marketing = models.FloatField()
    price_marketing_promotion = models.FloatField(default=0)
    type = models.CharField(default='V', max_length=1, choices=(
        ('V','Variance'),
        ('S','Simple'),
        ))

    #format the price
    def get_price_format(self):
        return f'€ {self.price_marketing:.2f}'.replace('.',',')
    get_price_format: get_price_format

    def get_price_promo_format(self):
        return f'€ {self.price_marketing_promotion:.2f}'.replace('.',',')
    get_price_promo_format: get_price_promo_format

    @staticmethod
    def resize_image(img, new_width=800):
        #obtan the img path
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        #open image
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size
       
        if original_width<= new_width:    
            #print('original with less than new width')
            img_pil.close()
            return 

        #calculate new size
        new_height = round((new_width * original_height) / original_width)
        new_img = img_pil.resize((new_width,new_height), Image.LANCZOS)
        new_img.save(img_full_path, optimize=True, quality=50)
        #print('image was resize')

        #print(original_width,original_height)

    # to resize image
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size=800
        if self.image:
            self.resize_image(self.image, max_image_size)

    #to appear the correct name of each product in the admin page
    def __str__(self):
        return self.name
    

class Variance(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name =  models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()
    price_promotion = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name or self.product.name
