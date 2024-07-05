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
<<<<<<< HEAD
    path('giamgia/<str:magiamgia>/', views.giamgia, name='giamgia_detail'),
    path('nhanvien/',views.nhanvien ,name="nhanvien"),
=======
>>>>>>> 6125e016e761516f36ad24c0f3b1db84b79b51dc
    path('order/',views.order ,name="order"),
    path('order/<str:madonhang>/', views.order, name='order_detail'),
    path('donhangdetail/',views.donhangdetail ,name="donhangdetail"),
    path('donhangdetail/<str:ma_donhang_detail>/', views.donhangdetail, name='donhangdetail_detail'),
    path('add_to_cart/<str:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('order-history/', views.order_history, name='order_history'),
    path('kho/',views.kho ,name="kho"),
    path('kho/<str:idkho>',views.kho ,name="kho_hh"),
    path('tonkho/',views.tonkho ,name="tonkho"),
    path('tonkho/<str:idtonkho>',views.tonkho ,name="tonkho_hh"),
    path('nhacungcap/',views.nhacungcap ,name="nhacungcap"),
    path('nhacungcap/<str:manhacungcap>',views.nhacungcap ,name="nhacungcap_hh"),
    path('ordernhacungcap/',views.ordernhacungcap ,name="ordernhacungcap"),
    path('ordernhacungcap/<str:idorder>',views.ordernhacungcap ,name="ordernhacungcap_hh"),
    path('nhanvien/<str:manhanvien>/', views.nhanvien, name='nhanvien_detail'),
    path('account/',views.account,name="account"),
    path('account/<str:idtaikhoan>/',views.account,name="account_detail"),
    path('nguoidung/',views.nguoidung ,name="nguoidung"),
    path('nguoidung/<str:manguoidung>/', views.nguoidung, name='nguoidung_detail'),
]   
