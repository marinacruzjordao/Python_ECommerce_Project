from django.urls import path
from . import views

app_name='product' #product:list

urlpatterns = [
    path('', views.ListProducts.as_view(), name="lists"),
    path('<slug>', views.DetailProduct.as_view(), name='detail'),
    path('addtocart/', views.AddToCart.as_view(), name='addtocart'),
    path('removefromcart/', views.RemoveFromCart.as_view(), name='removefromcart'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('finish/', views.Finish.as_view(), name='finish'),
    path('search/', views.Search.as_view(), name='search'),

]
