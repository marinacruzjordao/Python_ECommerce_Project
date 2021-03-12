from django.urls import path
from . import views

app_name='request'

urlpatterns = [
   path('', views.Pay.as_view(), name="pay"),
   path('closerequest/', views.CloseRequest.as_view(), name='closerequest'),
   path('detail/', views.Detail.as_view(), name='detail'),
]
