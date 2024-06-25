from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import *
from django.contrib.auth.forms import UserCreationForm
from django.apps import *
from .models import *
def home(request ):
    
    products = Nongsan.objects.select_related('madanhmuc').all()
    product_danhmuc = Nongsan.objects.all()
    categories = Danhmuc.objects.all()
   
    context = {
        'products': products,
        'categories': categories,
        ' product_danhmuc': product_danhmuc
    }
    return render(request, 'user/index.html', context)


def shop(request):
    context = {}
    return render(request, 'user/shop.html', context)

def contact(request):
    context = {}
    return render(request, 'user/contact.html', context)

def cart(request):
    context = {}
    return render(request, 'user/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'user/checkout.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = Taikhoan.objects.get(username=username, password=password)
        except Taikhoan.DoesNotExist:
            user = None
        
        if user is not None:
            request.session['checklogin'] = user.idtaikhoan
            
            try:
                nguoidung = Nguoidung.objects.get(idtaikhoan=user.idtaikhoan)
                request.session['khachHang_name'] = nguoidung.hovaten
                request.session['khachHang_email'] = nguoidung.email
                request.session['khachHang_image_url'] = nguoidung.image.url  # Store image URL instead of ImageFieldFile
                request.session['khachHang_address'] = nguoidung.diachi  # Store image URL instead of ImageFieldFile
                request.session['khachHang_phone'] = nguoidung.phone  # Store image URL instead of ImageFieldFile
                
            except Nguoidung.DoesNotExist:
                pass

            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return render(request, 'user/login.html', {'username': username})

    return render(request, 'user/login.html')


def register(request):
    #  if request.method == 'POST':
    #     form = RegistrationForm(request.POST)
    #     if form.is_valid():
    #         avatar_link = "https://europe1.discourse-cdn.com/arduino/original/4X/b/8/6/b866973d0a9738af645201b3c4f4e4fe30021450.png"
    #         name = form.cleaned_data['name']
    #         email = form.cleaned_data['email']
    #         address = form.cleaned_data['address']
    #         phone = form.cleaned_data['phone']
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']
    #         if len(password) < 8:
    #             messages.error(request, 'Mật khẩu phải có ít nhất 8 ký tự.')
    #             return render(request, 'register.html', {'form': form})
    #         if Users.objects.filter(token=username).exists():
    #             messages.error(request, 'Tên đăng nhập đã tồn tại.')
    #             return render(request, 'register.html', {'form': form})
    #         if Customer.objects.filter(email=email).exists():
    #             messages.error(request, 'Email đã tồn tại.')
    #             return render(request, 'register.html', {'form': form})
    #         user = Users.objects.create(
    #             avatar=avatar_link,
    #             account_type='customer',
    #             token=username,
    #             password=password,
    #             create_at=timezone.now(),
    #             update_at=timezone.now(),
    #             create_by='admin',
    #             update_by='admin'
    #         )
    #         customer = Customer.objects.create(
    #             id_user=user,
    #             name_customer=name,
    #             email=email,
    #             phone=phone,
    #             address=address
    #         )
    #         messages.success(request, 'Đăng ký thành công. Bạn có thể đăng nhập ngay bây giờ.')
    #         return redirect('login')  
    #     else:
    #         messages.error(request, 'Vui lòng kiểm tra lại thông tin đăng ký.')
    
    return render(request, 'user/register.html')
def profile(request):
    return render(request, 'user/profile.html')

def nongsan(request):
    context = {}
    return render(request, 'admin/nongsan.html', context)

def manage(request):
    context = {}
    return render(request, 'admin/adminpage.html', context)

def logout(request):
    if 'checklogin' in request.session:
        del request.session['checklogin']
    if 'customer_name' in request.session:
        del request.session['khachHang_name']
    return redirect('/')