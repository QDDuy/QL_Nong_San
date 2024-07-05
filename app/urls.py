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
    path('logout/',views.logout ,name="logout"),
    path('profile/',views.profile ,name="profile"),
    path('giamgia/',views.giamgia ,name="giamgia"),
    path('nhanvien/',views.nhanvien ,name="nhanvien"),
    path('order/',views.order ,name="order"),
    path('orderdetail/',views.orderdetail ,name="orderdetail"),
    path('add_to_cart/<str:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('order-history/', views.order_history, name='order_history'),
    path('nhanvien/<str:manhanvien>/', views.nhanvien, name='nhanvien_detail'),
    path('account/',views.account,name="account"),
    path('account/<str:idtaikhoan>/',views.account,name="account_detail"),
    path('nguoidung/',views.nguoidung ,name="nguoidung"),
    path('nguoidung/<str:manguoidung>/', views.nguoidung, name='nguoidung_detail'),
]   
