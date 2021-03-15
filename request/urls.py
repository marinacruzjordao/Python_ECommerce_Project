from django.urls import path
from . import views

app_name='request'

urlpatterns = [
   path('pay/<int:pk>', views.Pay.as_view(), name="pay"), #pk becausa received an id.
   path('saverequest/', views.SaveRequest.as_view(), name='saverequest'),
   path('lists/', views.Lists.as_view(), name='lists'),
   path('detail/<int:pk>', views.Detail.as_view(), name='detail'),
]

