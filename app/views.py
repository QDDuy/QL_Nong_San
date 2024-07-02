from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import *
from django.contrib.auth.forms import UserCreationForm
from django.apps import *
from .models import *
from django.contrib.auth.hashers import make_password,check_password
from django.db import transaction
from datetime import date
import uuid

def home(request ):
    
    products = Nongsan.objects.select_related('madanhmuc').all()
    product_danhmuc = Nongsan.objects.all()
    categories = Danhmuc.objects.all()
   
    context = {
        'products': products,
        'categories': categories,
        'product_danhmuc': product_danhmuc
    }
    return render(request, 'user/index.html', context)


def shop(request):
    query = request.GET.get('search', '')
    categories = Danhmuc.objects.all()

    if query:
        result = Nongsan.objects.filter(ten__icontains=query)
    else:
        result = Nongsan.objects.all()

    context = {
        'query': query,
        'result': result,
        'categories': categories
    }

    return render(request, 'user/shop.html', context)


def contact(request):
    context = {}
    return render(request, 'user/contact.html', context)





def cart(request):
    user_id = request.session.get('manguoidung')

    if user_id:
        # Lấy tất cả các mục trong giỏ hàng của người dùng đã đăng nhập
        cart_items = Cart.objects.filter(user_id=user_id)

        if not cart_items.exists():
            messages.info(request, 'Giỏ hàng của bạn đang trống.')
            return render(request, 'user/cart.html', {'cart_items': [], 'total_quantity': 0, 'total_price': 0})

        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.nongsan.gia * item.quantity for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_quantity': total_quantity,
            'total_price': total_price,
        }

        return render(request, 'user/cart.html', context)
    else:
        messages.error(request, 'Bạn chưa đăng nhập.')
        return redirect('login')  # Điều hướng đến trang đăng nhập nếu không có ID người dùng trong session
    
def checkout(request):
    user_id = request.session.get('manguoidung')
    
    if not user_id:
        messages.error(request, 'Bạn chưa đăng nhập.')
        return redirect('login')

    try:
        user = Nguoidung.objects.get(manguoidung=user_id)
        cart_items = Cart.objects.filter(user=user)

        if request.method == 'POST':
            shipping_address = request.POST.get('shipping_address')
            total_price = sum(item.nongsan.gia * item.quantity for item in cart_items)

            try:
                with transaction.atomic():
                    # Tạo đơn hàng mới
                    order = Donhang.objects.create(
                        madonhang=f"DH_{user_id}_{date.today().strftime('%Y%m%d')}",
                        manguoidung=user,
                        tonggia=total_price,
                        ngaydat=date.today(),
                        trangthai='Pending',  # Trạng thái đơn hàng
                    )

                    # Tạo chi tiết đơn hàng
                    for item in cart_items:
                        DonHangDetail.objects.create(
                            ma_donhang=order,
                            id_nongsan=item.nongsan,
                            quantity=item.quantity,
                        )

                    cart_items.delete()  # Xóa giỏ hàng sau khi tạo đơn hàng thành công

                messages.success(request, 'Đơn hàng của bạn đã được tạo thành công!')
                return redirect('home')  # Điều hướng đến trang chủ sau khi thanh toán thành công

            except Exception as e:
                messages.error(request, 'Đã xảy ra lỗi trong quá trình thanh toán. Vui lòng thử lại sau.')
                return redirect('checkout')  # Điều hướng lại trang thanh toán nếu có lỗi xảy ra

        context = {
            'cart_items': cart_items,
            'total_price': sum(item.nongsan.gia * item.quantity for item in cart_items),
        }
        return render(request, 'user/checkout.html', context)

    except Nguoidung.DoesNotExist:
        messages.error(request, 'Người dùng không tồn tại.')
        return redirect('login')  # Điều hướng người dùng đến trang đăng nhập nếu người dùng không tồn tại

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Taikhoan.objects.get(username=username)
            if check_password(password, user.password):  # Check password using Django's check_password
                request.session['checklogin'] = user.idtaikhoan
                print(f"User ID from Taikhoan: {user.idtaikhoan}")
                
                try:
                    nguoidung = Nguoidung.objects.get(idtaikhoan=user.idtaikhoan)
                    request.session['manguoidung'] = nguoidung.manguoidung
                    request.session['khachHang_name'] = nguoidung.hovaten
                    request.session['khachHang_email'] = nguoidung.email
                    request.session['khachHang_image_url'] = nguoidung.image.url if nguoidung.image else None
                    request.session['khachHang_address'] = nguoidung.diachi
                    request.session['khachHang_phone'] = nguoidung.phone
                    print(f"User information stored in session: {nguoidung.manguoidung}, {nguoidung.hovaten}")
                except Nguoidung.DoesNotExist:
                    print("Nguoidung does not exist for this user.")
                    pass

                return redirect('/')
            else:
                print("Invalid username or password.")
                messages.error(request, 'Invalid username or password. Please try again.')
                return render(request, 'user/login.html', {'username': username})
        
        except Taikhoan.DoesNotExist:
            print("User does not exist.")
            messages.error(request, 'User does not exist.')
            return render(request, 'user/login.html', {'username': username})

    return render(request, 'user/login.html')


def register(request):
    if request.method == 'POST':
        hovaten = request.POST.get('fullname')
        email = request.POST.get('email')
        diachi = request.POST.get('address')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        passwordConfirm = request.POST.get('passwordConfirm')
        
        if not all([hovaten, email, diachi, phone, username, password, passwordConfirm]):
            messages.error(request, 'Vui lòng điền đầy đủ thông tin.')
            return render(request, 'user/register.html')
        
        if password != passwordConfirm:
            messages.error(request, 'Mật khẩu và xác nhận mật khẩu không khớp.')
            return render(request, 'user/register.html')
        
        if len(password) < 8:
            messages.error(request, 'Mật khẩu phải có ít nhất 8 ký tự.')
            return render(request, 'user/register.html')
            
        if Taikhoan.objects.filter(username=username).exists():
            messages.error(request, 'Tên đăng nhập đã tồn tại.')
            return render(request, 'user/register.html')
            
        if Nguoidung.objects.filter(email=email).exists():
            messages.error(request, 'Email đã tồn tại.')
            return render(request, 'user/register.html')
            
        id_taikhoan = f"TK{uuid.uuid4()}"
        id_nguoidung = f"KH{uuid.uuid4()}"
        hashed_password = make_password(password)
        taikhoan = Taikhoan.objects.create(
            
            idtaikhoan=id_taikhoan,
            username=username,
            password=password,
            role='customer'
        )
        
        nguoidung = Nguoidung.objects.create(
            manguoidung=id_nguoidung,
            hovaten=hovaten,
            email=email,
            diachi=diachi,
            phone=phone,
            idtaikhoan=taikhoan
        )
        
        messages.success(request, 'Đăng ký thành công. Bạn có thể đăng nhập ngay bây giờ.')
        return redirect('login')
    return render(request, 'user/register.html')


def add_to_cart(request, product_id):
    id_user = request.session.get('manguoidung')
    product = get_object_or_404(Nongsan, idnongsan=product_id)
    
    # Mặc định số lượng là 1 khi dùng phương thức GET
    quantity = 1

    if id_user:
        try:
            customer = Nguoidung.objects.get(manguoidung=id_user)
            
            try:
                cart = Donhang.objects.get(manguoidung=customer, trangthai='Chưa thanh toán')
            except Donhang.DoesNotExist:
                madonhang = f"DH-{uuid.uuid4()}"
                cart = Donhang.objects.create(manguoidung=customer, madonhang=madonhang)

            # Tạo hoặc cập nhật chi tiết đơn hàng
            madonhangdetails = f"DHT-{uuid.uuid4()}"
            cart_detail, created = DonHangDetail.objects.get_or_create(
                ma_donhang_detail = madonhangdetails,
                ma_donhang=cart,
                id_nongsan=product,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_detail.quantity += quantity
                cart_detail.save()

            messages.success(request, 'Sản phẩm đã được thêm vào giỏ hàng.')
            return redirect('cart')

        except Nguoidung.DoesNotExist:
            messages.error(request, 'Không tìm thấy thông tin khách hàng.')
            return redirect('login')

    else:
        messages.error(request, 'Bạn chưa đăng nhập.')
        return redirect('login')
    
    
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