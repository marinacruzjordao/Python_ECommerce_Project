from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #when user is delete evrything is delete
    total = models.FloatField()
    status = models.CharField(  
        default = 'C',
        max_length=1,
        choices = (
            ('A', 'Approved'),
            ('C', 'Created'),
            ('R', 'Reject'),
            ('P', 'Pending'),
            ('S', 'Send'),
            ('F','Finalized'),
        )
    )

    #to show the name of request in admin page
    def __str__(self):
        return f'Request N. {self.pk}'

class ItemRequest(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField()
    variance = models.CharField(max_length=255)
    variance_id = models.PositiveIntegerField()
    price = models.FloatField()
    price_promotion = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)

      #to show the name of itemrequest in admin pagepk}'
    def __str__(self):
        return f'{self.request} item'