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
from django.db.models import Count
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
    category_id = request.GET.get('category', None)
    sort_by_price = request.GET.get('sort_by_price', None)

    categories = Danhmuc.objects.all()
    categories = Danhmuc.objects.annotate(num_products=Count('nongsan'))
    # Bộ lọc sản phẩm
    result = Nongsan.objects.all()

    if query:
        result = result.filter(ten__icontains=query)

    if category_id:
        result = result.filter(madanhmuc=category_id)

    if sort_by_price == 'ascending':
        result = result.order_by('gia')  # Sắp xếp từ thấp đến cao theo giá
    elif sort_by_price == 'descending':
        result = result.order_by('-gia')  # Sắp xếp từ cao đến thấp theo giá

    context = {
        'query': query,
        'result': result,
        'categories': categories,
        'current_category': category_id,
    }

    return render(request, 'user/shop.html', context)


def shop_detail(request,idnongsan):
    nongsan=get_object_or_404(Nongsan,idnongsan=idnongsan)
    
    return render(request, 'user/shop-detail.html',{'nongsan':nongsan})
def contact(request):
    context = {}
    return render(request, 'user/contact.html', context)





def cart(request):
    user_id = request.session.get('manguoidung')

    if user_id:
        cart_items = Cart.objects.filter(user_id=user_id)
        
        if not cart_items.exists():
            return render(request, 'user/cart.html', {'cart_items': [], 'total_quantity': 0, 'total_price': 0})

        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.nongsan.gia * item.quantity for item in cart_items)
        for item in cart_items:
            item.total_price = item.nongsan.gia * item.quantity
        context = {
            'cart_items': cart_items,
            'total_quantity': total_quantity,
            'total_price': total_price,
        }

        return render(request, 'user/cart.html', context)
    else:
        return redirect('login')  # Điều hướng đến trang đăng nhập nếu không có ID người dùng trong session


    
def checkout(request):
    user_id = request.session.get('manguoidung')
    
    if not user_id:
        messages.error(request, 'Bạn chưa đăng nhập.')
        return redirect('login')

    try:
        user = Nguoidung.objects.get(manguoidung=user_id)
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            messages.error(request, 'Giỏ hàng của bạn đang trống.')
            return redirect('cart')

        if request.method == 'POST':
            total_price = sum(item.nongsan.gia * item.quantity for item in cart_items)

            try:
                with transaction.atomic():
                    order = Donhang.objects.create(
                        madonhang=f"DH_{uuid.uuid4()}",
                        manguoidung=user,
                        tonggia=total_price,
                        ngaydat=date.today(),
                        trangthai='Pending',  
                    )

                    for item in cart_items:
                        DonHangDetail.objects.create(
                            ma_donhang_detail=uuid.uuid4().hex,
                            ma_donhang=order,
                            id_nongsan=item.nongsan,
                            quantity=item.quantity,
                        )

                    cart_items.delete()

                messages.success(request, 'Đơn hàng của bạn đã được tạo thành công!')
                return redirect('home')

            except Exception as e:
                print(f"Lỗi trong quá trình thanh toán: {str(e)}")  # In lỗi ra console
                messages.error(request, f'Đã xảy ra lỗi trong quá trình thanh toán. Vui lòng thử lại sau. Chi tiết lỗi: {str(e)}')
                return redirect('checkout')
        for item in cart_items:
            item.total_price = item.nongsan.gia * item.quantity
        context = {
            'cart_items': cart_items,
            'total_price': sum(item.nongsan.gia * item.quantity for item in cart_items),
        }
        return render(request, 'user/checkout.html', context)

    except Nguoidung.DoesNotExist:
        messages.error(request, 'Người dùng không tồn tại.')
        return redirect('login')
    
    
    
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
                    
                    if nguoidung.image:
                        try:
                            image_url = nguoidung.image.url
                            print(f"Image URL: {image_url}")
                            request.session['khachHang_image_url'] = image_url
                        except Exception as e:
                            print(f"Error accessing image URL: {e}")
                            request.session['khachHang_image_url'] = None
                    else:
                        request.session['khachHang_image_url'] = None
                    
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
            password=hashed_password,
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
    user_id = request.session.get('manguoidung')
    
    if user_id:
        user = get_object_or_404(Nguoidung, manguoidung=user_id)
    else:
        return redirect('login')  
    nongsan = get_object_or_404(Nongsan, idnongsan=product_id)
    quantity = 1
    try:
        cart_item = Cart.objects.get(user=user, nongsan=nongsan)
        cart_item.quantity += quantity
        cart_item.save()
    except Cart.DoesNotExist:
        cart_id = f"cart-{uuid.uuid4()}"
        Cart.objects.create(
            cart_id=cart_id,
            user=user,
            nongsan=nongsan,
            quantity=quantity
        )

    return redirect('cart')

    
    
def profile(request):
    action=request.GET.get('action')
    if(action=='update'):
        id_user=request.session.get('manguoidung')
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        try:
            nguoidung = Nguoidung.objects.get(manguoidung=id_user)
            nguoidung.fullname = fullname
            nguoidung.email = email
            nguoidung.phone = phone
            nguoidung.address = address
            nguoidung.save()
            request.session['khachHang_name'] = fullname
            request.session['khachHang_email'] = email
            request.session['khachHang_phone'] = phone
            request.session['khachHang_address'] = address
            messages.success(request, 'Thông tin người dùng đã được cập nhật thành công.')
            return render(request, 'user/profile.html')  # Redirect về trang profile sau khi cập nhật thành công
        except Nguoidung.DoesNotExist:
            messages.error(request, 'Người dùng không tồn tại.')
            return redirect('profile')
    
    elif action == 'changeAvatar' and request.method == 'POST':
        id_user = request.session.get('manguoidung')
        avatar = request.FILES.get('avatar')  # Lấy tệp tải lên
        
        try:
            nguoidung = Nguoidung.objects.get(manguoidung=id_user)
            nguoidung.image = avatar  # Gán tệp tải lên cho trường image
            nguoidung.save()
            request.session['khachHang_image_url']=nguoidung.image.url
            messages.success(request, 'Ảnh đại diện đã được thay đổi thành công.')
            return redirect('profile')
        except Nguoidung.DoesNotExist:
            messages.error(request, 'Người dùng không tồn tại.')
            return redirect('profile')
    return render(request, 'user/profile.html')


def order_history(request):
    user_id = request.session.get('manguoidung')
    
    if not user_id:
        return redirect('login')  # Nếu người dùng chưa đăng nhập, điều hướng đến trang đăng nhập

    try:
        orders = Donhang.objects.filter(manguoidung=user_id).order_by('-ngaydat')  # Lấy các đơn hàng của người dùng đã đặt
    
        context = {
            'orders': orders,
        }
        return render(request, 'user/orderHistory.html', context)

    except Nguoidung.DoesNotExist:
        return redirect('login') 
    

def nongsan(request):
    context = {}
    return render(request, 'admin/nongsan.html', context)



def giamgia(request):
    context = {}
    return render(request, 'admin/giamgia.html', context)

def order(request):
    context = {}
    return render(request, 'admin/order.html', context)

def orderdetail(request):
    context = {}
    return render(request, 'admin/orderdetail.html', context)

def manage(request):
    context = {}
    return render(request, 'admin/adminpage.html', context)

def logout(request):
    if 'checklogin' in request.session:
        del request.session['checklogin']
    if 'customer_name' in request.session:
        del request.session['khachHang_name']
    return redirect('/')


def nhanvien(request, manhanvien=None):
    if request.method == 'GET':
        url = request.GET.get('url')
        if url == "deleteNV" and manhanvien:
            try:
                nhanvien_instance = get_object_or_404(Nhanvien, manhanvien=manhanvien)
                nhanvien_instance.delete()
                messages.success(request, 'Nhân viên đã được xóa thành công.')
                return redirect('nhanvien')
            except Nhanvien.DoesNotExist:
                messages.error(request, 'Không tìm thấy nhân viên.')
                return redirect('nhanvien')

        # Hiển thị danh sách nhân viên
        nhanviens = Nhanvien.objects.all()
        return render(request, 'admin/nhanvien.html', {'nhanviens': nhanviens})

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == "insertNV":
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            salary = request.POST.get('salary')
            shift = request.POST.get('shift')
            accountId = request.POST.get('accountId')
            Image = request.POST.get('Image')

            try:
                taikhoan_instance = Taikhoan.objects.get(idtaikhoan=accountId)
            except Taikhoan.DoesNotExist:
                messages.error(request, 'Không tìm thấy tài khoản.')
                return redirect('nhanvien')

            nhanvienid = f"NV-{str(uuid.uuid4())[:5]}"
            Nhanvien.objects.create(
                manhanvien=nhanvienid,
                tennhanvien=name,
                email=email,
                sodienthoai=phone,
                luong=salary,
                calamviec=shift,
                idtaikhoan=taikhoan_instance,
                image=Image
            )
            messages.success(request, 'Nhân viên mới đã được thêm thành công.')
            return redirect('nhanvien')

        elif action == "editNV" and manhanvien:
            try:
                nhanvien = get_object_or_404(Nhanvien, manhanvien=manhanvien)
                taikhoan_instance = get_object_or_404(Taikhoan, idtaikhoan=request.POST.get('accountId'))
                nhanvien.tennhanvien = request.POST.get('name')
                nhanvien.email = request.POST.get('email')
                nhanvien.sodienthoai = request.POST.get('phone')
                nhanvien.luong = request.POST.get('salary')
                nhanvien.calamviec = request.POST.get('shift')
                nhanvien.image = request.POST.get('Image')
                nhanvien.idtaikhoan = taikhoan_instance
                nhanvien.save()
                messages.success(request, 'Thông tin nhân viên đã được cập nhật thành công.')
                return redirect('nhanvien')
            except Nhanvien.DoesNotExist:
                messages.error(request, 'Không tìm thấy nhân viên.')
                return redirect('nhanvien')
            except Taikhoan.DoesNotExist:
                messages.error(request, 'Không tìm thấy tài khoản.')
                return redirect('nhanvien')

    return redirect('nhanvien')


def account(request, idtaikhoan=None):
    if request.method == 'GET':
        url = request.GET.get('url')
        if url == "deleteAcc" and idtaikhoan:
            try:
                taikhoan = get_object_or_404(Taikhoan, idtaikhoan=idtaikhoan)
                taikhoan.delete()
                messages.success(request, 'Nhân viên đã được xóa thành công.')
                return redirect('account')
            except Nhanvien.DoesNotExist:
                messages.error(request, 'Không tìm thấy nhân viên.')
                return redirect('account')

        # Hiển thị danh sách nhân viên
        accounts = Taikhoan.objects.all()
        return render(request, 'admin/account.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == "insertAcc":
            username = request.POST.get('username')
            password = request.POST.get('password')
            role = request.POST.get('role')

            idaccount= f"TK-{str(uuid.uuid4())[:5]}"
            hashed_password = make_password(password)
            
            Taikhoan.objects.create(
                idtaikhoan=idaccount,
                username=username,
                password=hashed_password,
                role=role,
            )
            messages.success(request, 'Thêm tài khoản thành công.')
            return redirect('account')

        elif action == "editAcc" and idtaikhoan:
            try:
                taikhoan = get_object_or_404(Taikhoan, idtaikhoan=idtaikhoan)
                taikhoan.tennhanvien = request.POST.get('username')
                taikhoan.email = request.POST.get('password')
                taikhoan.role = request.POST.get('role')
                taikhoan.save()
                messages.success(request, 'Thông tin tài khoản đã được cập nhật thành công.')
                return redirect('account')
            except Nhanvien.DoesNotExist:
                messages.error(request, 'Không tìm thấy nhân viên.')
                return redirect('account')
            except Taikhoan.DoesNotExist:
                messages.error(request, 'Không tìm thấy tài khoản.')
                return redirect('account')

    return redirect('account')



def nguoidung(request, manguoidung=None):
    if request.method == 'GET':
        url = request.GET.get('url')
        if url == "deleteND" and manguoidung:
            try:
                nguoidung = get_object_or_404(Nguoidung, manguoidung=manguoidung)
                nguoidung.delete()
                messages.success(request, 'Người dùng đã được xóa thành công.')
                return redirect('nguoidung')
            except Nguoidung.DoesNotExist:
                messages.error(request, 'Không tìm thấy người dùng.')
                return redirect('nguoidung')

        # Hiển thị danh sách nhân viên
        users = Nguoidung.objects.all()
        return render(request, 'admin/nguoidung.html', {'users': users})

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == "insertND":
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            accountId = request.POST.get('accountId')
            Image = request.POST.get('Image')

            try:
                taikhoan_instance = Taikhoan.objects.get(idtaikhoan=accountId)
            except Taikhoan.DoesNotExist:
                messages.error(request, 'Không tìm thấy tài khoản.')
                return redirect('nguoidung')

            idnguoidung = f"ND-{str(uuid.uuid4())[:5]}"
            Nguoidung.objects.create(
                manguoidung=idnguoidung,
                hovaten=name,
                email=email,
                phone=phone,
                diachi=address,
                idtaikhoan=taikhoan_instance,
                image=Image
            )
            messages.success(request, 'Người dùng đã được thêm thành công.')
            return redirect('nguoidung')

        elif action == "editND" and manguoidung:
            try:
                nguoidung = get_object_or_404(Nguoidung, manguoidung=manguoidung)
                taikhoan_instance = get_object_or_404(Taikhoan, idtaikhoan=request.POST.get('accountId'))
                nguoidung.hovaten = request.POST.get('name')
                manguoidung.email = request.POST.get('email')
                manguoidung.phone = request.POST.get('phone')
                manguoidung.diachi = request.POST.get('address')
                manguoidung.image = request.POST.get('Image')
                manguoidung.idtaikhoan = taikhoan_instance
                manguoidung.save()
                messages.success(request, 'Thông tin người dùng đã được cập nhật thành công.')
                return redirect('nguoidung')
            except Nguoidung.DoesNotExist:
                messages.error(request, 'Không tìm thấy người dùng.')
                return redirect('nguoidung')
            except Taikhoan.DoesNotExist:
                messages.error(request, 'Không tìm thấy tài khoản.')
                return redirect('nguoidung')

    return redirect('nguoidung')
