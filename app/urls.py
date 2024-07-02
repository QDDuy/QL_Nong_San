from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('shop/',views.shop,name="shop"),
    path('contact/',views.contact,name="contact"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    path('manage/',views.manage,name="manage"),
    path('nongsan/',views.nongsan,name="nongsan"),
    path('logout/',views.logout ,name="logout"),
    path('profile/',views.profile ,name="profile"),
    path('add_to_cart/<str:product_id>/', views.add_to_cart, name='add_to_cart'),
]   
