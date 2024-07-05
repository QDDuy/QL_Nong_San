from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('shop/',views.shop,name="shop"),
    path('shop-detail/<str:idnongsan>/', views.shop_detail, name='shop-detail'),
    path('contact/',views.contact,name="contact"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    path('manage/',views.manage,name="manage"),
    path('nongsan/',views.nongsan,name="nongsan"),
    path('nongsan/<str:IdNongSan>/', views.nongsan, name='nongsan_detail'),
    path('logout/',views.logout ,name="logout"),
    path('profile/',views.profile ,name="profile"),
    path('giamgia/',views.giamgia ,name="giamgia"),
    path('giamgia/<str:magiamgia>/', views.giamgia, name='giamgia_detail'),
    path('nhanvien/',views.nhanvien ,name="nhanvien"),
    path('order/',views.order ,name="order"),
    path('order/<str:madonhang>/', views.order, name='order_detail'),
    path('donhangdetail/',views.donhangdetail ,name="donhangdetail"),
    path('donhangdetail/<str:ma_donhang_detail>/', views.donhangdetail, name='donhangdetail_detail'),
    path('add_to_cart/<str:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('order-history/', views.order_history, name='order_history'),
    path('nhanvien/<str:manhanvien>/', views.nhanvien, name='nhanvien_detail'),
]   
