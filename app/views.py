from email.utils import parsedate
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
from django.utils.dateparse import parse_date
from django.db.models import Count
from django.db.models import F, ExpressionWrapper, DecimalField, Value,Case,When,Sum,IntegerField
from django.db.models.functions import Coalesce


def home(request):
    # Lấy tất cả sản phẩm kèm danh mục của chúng (sử dụng select_related để tối ưu hóa)
    products = Nongsan.objects.select_related('madanhmuc').all()

    # Lấy danh sách tất cả sản phẩm (không cần select_related ở đây nếu chỉ cần thông tin từ bảng Nongsan)
    product_danhmuc = Nongsan.objects.all()

    # Lấy tất cả danh mục
    categories = Danhmuc.objects.all()

    # Truy vấn sản phẩm bán chạy nhất từ các đơn hàng đã hoàn tất
    best_selling_products = Nongsan.objects.annotate(
        total_sold=Sum(
            Case(
                When(
                    donhangdetail__ma_donhang__trangthai='Completed',
                    then=F('donhangdetail__quantity')
                ),
                default=0,
                output_field=IntegerField()
            )
        )
    ).order_by('-total_sold')[:10]  # Lấy 10 sản phẩm bán chạy nhất

    # Bộ lọc và áp dụng giảm giá nếu có
    today = date.today()
    result = Nongsan.objects.all().annotate(
        gia_da_giam=Case(
            When(
                giamgia__ngaybatdau__lte=today,
                giamgia__ngayketthuc__gte=today,
                then=ExpressionWrapper(
                    F('gia') * (1 - F('giamgia__phantramgiam') / 100),
                    output_field=DecimalField(max_digits=15, decimal_places=2)
                )
            ),
            default=F('gia'),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        ),
        giamgia_hieu_luc=Case(
            When(
                giamgia__ngaybatdau__lte=today,
                giamgia__ngayketthuc__gte=today,
                then=Value(True)
            ),
            default=Value(False),
            output_field=IntegerField()
        )
    )

    context = {
        'products': products,
        'categories': categories,
        'product_danhmuc': product_danhmuc,
        'best_selling_products': best_selling_products,
        'result': result,
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

    # Áp dụng giảm giá nếu có
    today = date.today()
    result = result.annotate(
        gia_da_giam=Case(
            When(
                giamgia__ngaybatdau__lte=today,
                giamgia__ngayketthuc__gte=today,
                then=ExpressionWrapper(
                    F('gia') * (1 - Coalesce(F('giamgia__phantramgiam'), Value(0)) / 100),
                    output_field=DecimalField(max_digits=15, decimal_places=2)
                )
            ),
            default=F('gia'),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        ),
        giamgia_hieu_luc=Case(
            When(
                giamgia__ngaybatdau__lte=today,
                giamgia__ngayketthuc__gte=today,
                then=Value(True)
            ),
            default=Value(False),
            output_field=DecimalField()
        )
    )

    if sort_by_price == 'ascending':
        result = result.order_by('gia_da_giam')  # Sắp xếp từ thấp đến cao theo giá đã giảm
    elif sort_by_price == 'descending':
        result = result.order_by('-gia_da_giam')  # Sắp xếp từ cao đến thấp theo giá đã giảm

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

def nhanvien(request, manhanvien=None):
    if request.session.get('user_role') != 'admin':
        return redirect('/login/')  # Chuyển hướng đến trang đăng nhập nếu không phải admin

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


def cart(request):
    user_id = request.session.get('manguoidung')

    if user_id:
        cart_items = Cart.objects.filter(user_id=user_id).select_related('nongsan')
        
        if not cart_items.exists():
            return render(request, 'user/cart.html', {'cart_items': [], 'total_quantity': 0, 'total_price': 0})

        today = date.today()

        total_quantity = 0
        total_price = 0

        for item in cart_items:
            nongsan = item.nongsan
            gia_da_giam = Nongsan.objects.annotate(
                gia_da_giam=Case(
                    When(
                        giamgia__ngaybatdau__lte=today,
                        giamgia__ngayketthuc__gte=today,
                        then=ExpressionWrapper(
                            F('gia') * (1 - F('giamgia__phantramgiam') / 100),
                            output_field=DecimalField(max_digits=15, decimal_places=2)
                        )
                    ),
                    default=F('gia'),
                    output_field=DecimalField(max_digits=15, decimal_places=2)
                )
            ).get(idnongsan=nongsan.idnongsan).gia_da_giam

            item.price = gia_da_giam
            item.total_price = gia_da_giam * item.quantity
            total_quantity += item.quantity
            total_price += item.total_price

        context = {
            'cart_items': cart_items,
            'total_quantity': total_quantity,
            'total_price': total_price,
        }

        return render(request, 'user/cart.html', context)
    else:
        return redirect('login') # Điều hướng đến trang đăng nhập nếu không có ID người dùng trong session


    
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
            total_price = 0
            for item in cart_items:
                giamgia = Giamgia.objects.filter(idnongsan=item.nongsan).first()
                if giamgia and giamgia.ngayketthuc and giamgia.ngaybatdau <= date.today() <= giamgia.ngayketthuc:
                    gia_da_giam = item.nongsan.gia * (1 - giamgia.phantramgiam / 100)
                    total_price += gia_da_giam * item.quantity
                else:
                    total_price += item.nongsan.gia * item.quantity

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
                print(f"Lỗi trong quá trình thanh toán: {str(e)}")
                messages.error(request, f'Đã xảy ra lỗi trong quá trình thanh toán. Vui lòng thử lại sau. Chi tiết lỗi: {str(e)}')
                return redirect('checkout')

        total_price = 0
        for item in cart_items:
            giamgia = Giamgia.objects.filter(idnongsan=item.nongsan).first()
            if giamgia and giamgia.ngayketthuc and giamgia.ngaybatdau <= date.today() <= giamgia.ngayketthuc:
                gia_da_giam = item.nongsan.gia * (1 - giamgia.phantramgiam / 100)
                item.total_price = gia_da_giam * item.quantity
            else:
                item.total_price = item.nongsan.gia * item.quantity
            total_price += item.total_price

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
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
                request.session['user_role'] = user.role
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

                if user.role == 'admin': 
                    return redirect('nhanvien')  
                else:
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

    # Tính giá đã giảm (nếu có)
    today = date.today()
    gia_da_giam = Nongsan.objects.annotate(
        gia_da_giam=Case(
            When(
                giamgia__ngaybatdau__lte=today,
                giamgia__ngayketthuc__gte=today,
                then=ExpressionWrapper(
                    F('gia') * (1 - F('giamgia__phantramgiam') / 100),
                    output_field=DecimalField(max_digits=15, decimal_places=2)
                )
            ),
            default=F('gia'),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        )
    ).get(idnongsan=product_id).gia_da_giam

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

    # Thêm giá đã giảm vào session hoặc context để sử dụng sau này
    request.session['gia_da_giam'] = float(gia_da_giam)
    
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
            nguoidung.hovaten = fullname
            nguoidung.email = email
            nguoidung.phone = phone
            nguoidung.diachi = address
            nguoidung.save()
          
            messages.success(request, 'Thông tin người dùng đã được cập nhật thành công.')
            request.session['khachHang_name'] = fullname
            request.session['khachHang_email'] = email
            request.session['khachHang_phone'] = phone
            request.session['khachHang_address'] = address
            return render(request, 'user/profile.html') 
        except Nguoidung.DoesNotExist:
            messages.error(request, 'Người dùng không tồn tại.')
            return redirect('profile')
    
    elif action == 'changeAvatar' and request.method == 'POST':
        id_user = request.session.get('manguoidung')
        avatar = request.FILES.get('avatar')  # Lấy tệp tải lên

        try:
            nguoidung = Nguoidung.objects.get(manguoidung=id_user)
            
            # Kiểm tra xem ảnh đại diện mới đã tồn tại trong cơ sở dữ liệu chưa
            if Nguoidung.objects.filter(image=avatar.name).exists():
                messages.warning(request, 'Ảnh đại diện này bạn đang dùng.')
            else:
                nguoidung.image = avatar  # Gán tệp tải lên cho trường image
                nguoidung.save()
                request.session['khachHang_image_url'] = nguoidung.image.url
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


def manage(request):
    if request.session.get('user_role') != 'admin':
        return redirect('/login/') 
    context = {}
    return render(request, 'user/login.html', context)


def logout(request):
    if 'checklogin' in request.session:
        del request.session['checklogin']
    if 'customer_name' in request.session:
        del request.session['khachHang_name']
    return redirect('/')


def kho(request, idkho=None):
    if request.session.get('user_role') != 'admin':
        return redirect('/login/') 
    if request.method == 'GET':
        url = request.GET.get('url')
        if url == "deletekho" and idkho:
            try:
                kho_instance = get_object_or_404(Kho, idkho=idkho)
                kho_instance.delete()
                messages.success(request, 'Kho đã được xóa thành công.')
                return redirect('kho')
            except Kho.DoesNotExist:
                messages.error(request, 'Không tìm thấy kho.')
                return redirect('kho')
        # Hiển thị danh sách kho
        khos = Kho.objects.all()
        return render(request, 'admin/kho.html', {'khos': khos})
    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == "insertkho":
            name = request.POST.get('name')
            diachi = request.POST.get('diachi')
            khoid = f"K-{str(uuid.uuid4())[:5]}"
            Kho.objects.create(
                idkho=khoid,
                name=name,
                diachi=diachi,
                
            )
            messages.success(request, 'Kho mới đã được thêm thành công.')
            return redirect('kho')
            

        elif action == "editkho" and idkho:
            try:
                kho = get_object_or_404(Kho, idkho=idkho)
                
                kho.name = request.POST.get('name')
                kho.diachi = request.POST.get('diachi')
                kho.save()
                messages.success(request, 'Thông tin kho đã được cập nhật thành công.')
                return redirect('kho')
            except Kho.DoesNotExist:
                messages.error(request, 'Không tìm thấy kho.')
                return redirect('kho')

def nongsan(request, IdNongSan=None):
    if request.session.get('user_role') != 'admin':
        return redirect('/login/') 
    if request.method == 'GET':
        url = request.GET.get('action')
        if url == "deleteNS" and IdNongSan:
            try:
                nongsan_instance = get_object_or_404(Nongsan, idnongsan=IdNongSan)
                nongsan_instance.delete()
                messages.success(request, 'Nông sản đã được xóa thành công.')
                return redirect('nongsan')
            except Nongsan.DoesNotExist:
                messages.error(request, 'Không tìm thấy nông sản.')
                return redirect('nongsan')

        # Hiển thị danh sách nông sản
        nongsans = Nongsan.objects.all()
        danhmucs = Danhmuc.objects.all()
        return render(request, 'admin/nongsan.html', {'nongsans': nongsans, 'danhmucs': danhmucs})

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == "insertNS":
            ten = request.POST.get('ten')
            mota = request.POST.get('mota')
            gia = request.POST.get('gia')
            trongluong = request.POST.get('trongluong')
            madanhmuc = request.POST.get('madanhmuc')
            image = request.FILES.get('image')

            nongsan_id = f"NS-{str(uuid.uuid4())[:5]}"
            Nongsan.objects.create(
                idnongsan=nongsan_id,
                ten=ten,
                mota=mota,
                gia=gia,
                trongluong=trongluong,
                madanhmuc=Danhmuc.objects.get(madanhmuc=madanhmuc),
                image=image
            )
            messages.success(request, 'Nông sản mới đã được thêm thành công.')
            return redirect('nongsan')

        elif action == "editNS" and IdNongSan:
            try:
                nongsan = get_object_or_404(Nongsan, idnongsan=IdNongSan)
                
                nongsan.ten = request.POST.get('ten')
                nongsan.mota = request.POST.get('mota')
                nongsan.gia = request.POST.get('gia')
                nongsan.trongluong = request.POST.get('trongluong')
                nongsan.madanhmuc = Danhmuc.objects.get(madanhmuc=request.POST.get('madanhmuc'))
                if request.FILES.get('image'):
                    nongsan.image = request.FILES.get('image')
                nongsan.save()
                messages.success(request, 'Thông tin nông sản đã được cập nhật thành công.')
                return redirect('nongsan')
            except Nongsan.DoesNotExist:
                messages.error(request, 'Không tìm thấy nông sản.')
                return redirect('nongsan')

    return redirect('nongsan')



def order(request, madonhang=None):
    if request.session.get('user_role') != 'admin':
        return redirect('/login/') 
    if request.method == 'GET':
        url = request.GET.get('action')
        if url == "deleteDH" and madonhang:
            try:
                donhang_instance = get_object_or_404(Donhang, madonhang=madonhang)
                donhang_instance.delete()
                messages.success(request, 'Đơn hàng đã được xóa thành công.')
                return redirect('order')
            except Donhang.DoesNotExist:
                messages.error(request, 'Không tìm thấy đơn hàng.')
                return redirect('order')

        # Hiển thị danh sách đơn hàng
        donhangs = Donhang.objects.all()
        nguoidungs = Nguoidung.objects.all()  # Lấy danh sách người dùng để hiển thị trong form
        return render(request, 'admin/order.html', {'donhangs': donhangs, 'nguoidungs': nguoidungs})

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == "insertDH":
            manguoidung = request.POST.get('manguoidung')
            tonggia = request.POST.get('tonggia')
            ngaydat = request.POST.get('ngaydat')
            trangthai = request.POST.get('trangthai')

            try:
                nguoidung_instance = Nguoidung.objects.get(manguoidung=manguoidung)
            except Nguoidung.DoesNotExist:
                messages.error(request, 'Không tìm thấy người dùng.')
                return redirect('order')

            donhangid = f"DH-{str(uuid.uuid4())[:5]}"
            Donhang.objects.create(
                madonhang=donhangid,
                manguoidung=nguoidung_instance,
                tonggia=tonggia,
                ngaydat=ngaydat,
                trangthai=trangthai
            )
            messages.success(request, 'Đơn hàng mới đã được thêm thành công.')
            return redirect('order')

        elif action == "editDH" and madonhang:
            try:
                donhang_instance = get_object_or_404(Donhang, madonhang=madonhang)
                nguoidung_instance = get_object_or_404(Nguoidung, manguoidung=request.POST.get('manguoidung'))

                ngaydat = request.POST.get('ngaydat')  # Đảm bảo biến ngaydat được gán giá trị trước khi sử dụng
                
                donhang_instance.manguoidung = nguoidung_instance
                donhang_instance.tonggia = request.POST.get('tonggia')
                donhang_instance.ngaydat = ngaydat
                donhang_instance.trangthai = request.POST.get('trangthai')
                donhang_instance.save()
                messages.success(request, 'Thông tin đơn hàng đã được cập nhật thành công.')
                return redirect('order')
            except Donhang.DoesNotExist:
                messages.error(request, 'Không tìm thấy đơn hàng.')
                return redirect('order')
            except Nguoidung.DoesNotExist:
                messages.error(request, 'Không tìm thấy người dùng.')
                return redirect('order')

    return redirect('order')




def donhangdetail(request, ma_donhang_detail=None):
    if request.session.get('user_role') != 'admin':
        return redirect('/login/') 
    if request.method == 'GET':
        url = request.GET.get('action')
        if url == "deleteDHDT" and ma_donhang_detail:
            try:
                donhangdetail_instance = get_object_or_404(DonHangDetail, ma_donhang_detail=ma_donhang_detail)
                donhangdetail_instance.delete()
                messages.success(request, 'Đơn hàng đã được xóa thành công.')
            except DonHangDetail.DoesNotExist:
                messages.error(request, 'Không tìm thấy chi tiết đơn hàng.')
            return redirect('donhangdetail')

        # Hiển thị danh sách chi tiết đơn hàng
        donhangdetails = DonHangDetail.objects.all()
        donhangs = Donhang.objects.all()
        nongsans = Nongsan.objects.all()
        return render(request, 'admin/orderdetail.html', {'donhangdetails': donhangdetails, 'donhangs': donhangs, 'nongsans': nongsans})

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == "insertCTDH":  # Sửa giá trị của action để khớp với form
            ma_donhang = request.POST.get('ma_donhang')
            id_nongsan = request.POST.get('id_nongsan')
            quantity = request.POST.get('quantity')

            try:
                donhang_instance = Donhang.objects.get(madonhang=ma_donhang)
                nongsan_instance = Nongsan.objects.get(idnongsan=id_nongsan)
                ma_donhang_detail = f"CTDH-{str(uuid.uuid4())[:5]}"
                DonHangDetail.objects.create(
                    ma_donhang_detail=ma_donhang_detail,
                    ma_donhang=donhang_instance,
                    id_nongsan=nongsan_instance,
                    quantity=quantity
                )
                messages.success(request, 'Đơn hàng mới đã được thêm thành công.')
            except Donhang.DoesNotExist:
                messages.error(request, 'Không tìm thấy đơn hàng.')
            except Nongsan.DoesNotExist:
                messages.error(request, 'Không tìm thấy nông sản.')

            return redirect('donhangdetail')

        elif action == "editCTDH" and ma_donhang_detail:
            try:
                donhangdetail_instance = get_object_or_404(DonHangDetail, ma_donhang_detail=ma_donhang_detail)
                donhang_instance = get_object_or_404(Donhang, madonhang=request.POST.get('ma_donhang'))
                nongsan_instance = get_object_or_404(Nongsan, idnongsan=request.POST.get('id_nongsan'))

                donhangdetail_instance.ma_donhang = donhang_instance
                donhangdetail_instance.id_nongsan = nongsan_instance
                donhangdetail_instance.quantity = request.POST.get('quantity')
                donhangdetail_instance.save()

                messages.success(request, 'Thông tin chi tiết đơn hàng đã được cập nhật thành công.')
            except DonHangDetail.DoesNotExist:
                messages.error(request, 'Không tìm thấy chi tiết đơn hàng.')
            except Donhang.DoesNotExist:
                messages.error(request, 'Không tìm thấy đơn hàng.')
            except Nongsan.DoesNotExist:
                messages.error(request, 'Không tìm thấy nông sản.')

            return redirect('donhangdetail')

    return redirect('donhangdetail')



def giamgia(request, magiamgia=None):
    if request.session.get('user_role') != 'admin':
        return redirect('/login/') 
    if request.method == 'GET':
        url = request.GET.get('action')
        if url == "deleteGG" and magiamgia:
            try:
                giamgia_instance = get_object_or_404(Giamgia, magiamgia=magiamgia)
                giamgia_instance.delete()
                messages.success(request, 'Thông tin giảm giá đã được xóa thành công.')
                return redirect('giamgia')
            except Giamgia.DoesNotExist:
                messages.error(request, 'Không tìm thấy thông tin giảm giá.')
                return redirect('giamgia')

        # Hiển thị danh sách giảm giá
        giamgias = Giamgia.objects.all()
        nongsans = Nongsan.objects.all()  # Lấy danh sách nông sản để hiển thị trong form
        return render(request, 'admin/giamgia.html', {'giamgias': giamgias, 'nongsans': nongsans})

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == "insertGG":
            idnongsan = request.POST.get('idnongsan')
            phantramgiam = request.POST.get('phantramgiam')
            ngaybatdau = request.POST.get('ngaybatdau')
            ngayketthuc = request.POST.get('ngayketthuc')
            mota = request.POST.get('mota')

            try:
                nongsan_instance = Nongsan.objects.get(idnongsan=idnongsan)
            except Nongsan.DoesNotExist:
                messages.error(request, 'Không tìm thấy nông sản.')
                return redirect('giamgia')

            magiamgia = f"GG-{str(uuid.uuid4())[:5]}"
            Giamgia.objects.create(
                magiamgia=magiamgia,
                idnongsan=nongsan_instance,
                phantramgiam=phantramgiam,
                ngaybatdau=ngaybatdau,
                ngayketthuc=ngayketthuc,
                mota=mota
            )
            messages.success(request, 'Thông tin giảm giá mới đã được thêm thành công.')
            return redirect('giamgia')

        elif action == "editGG" and magiamgia:
            try:
                giamgia_instance = get_object_or_404(Giamgia, magiamgia=magiamgia)
                nongsan_instance = get_object_or_404(Nongsan, idnongsan=request.POST.get('idnongsan'))

                giamgia_instance.idnongsan = nongsan_instance
                giamgia_instance.phantramgiam = request.POST.get('phantramgiam')
                giamgia_instance.ngaybatdau = request.POST.get('ngaybatdau')
                giamgia_instance.ngayketthuc = request.POST.get('ngayketthuc')
                giamgia_instance.mota = request.POST.get('mota')
                giamgia_instance.save()
                messages.success(request, 'Thông tin giảm giá đã được cập nhật thành công.')
                return redirect('giamgia')
            except Giamgia.DoesNotExist:
                messages.error(request, 'Không tìm thấy thông tin giảm giá.')
                return redirect('giamgia')
            except Nongsan.DoesNotExist:
                messages.error(request, 'Không tìm thấy nông sản.')
                return redirect('giamgia')

    return redirect('giamgia')


def tonkho(request, idtonkho=None):
    if request.session.get('user_role') != 'admin':
        return redirect('/login/') 
    if request.method == 'GET':
        url = request.GET.get('url')
        if url == "deleteTK" and idtonkho:
            try:
                tonkho_instance = get_object_or_404(Tonkho, idtonkho=idtonkho)
                tonkho_instance.delete()
                messages.success(request, 'Tồn Kho đã được xóa thành công.')
                return redirect('tonkho')
            except Tonkho.DoesNotExist:
                messages.error(request, 'Không tìm thấy tồn kho.')
                return redirect('tonkho')
     
        tonkhos = Tonkho.objects.all()
           # Gọi hàm notify_low_stock để kiểm tra và hiển thị thông báo
        for tonkho in tonkhos:
            notify_low_stock(request, tonkho)
        khos = Kho.objects.all()
        nongsans = Nongsan.objects.all()
        return render(request, 'admin/tonkho.html', {'tonkhos': tonkhos, 'nongsans' : nongsans, 'khos':khos})

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == "insertTK":
            idnongsan = request.POST.get('idnongsan')
            idkho = request.POST.get('idkho')
            soluong = request.POST.get('soluong')
            ngaynhapvao = request.POST.get('ngaynhapvao')
            ngayhethan = request.POST.get('ngayhethan')

            try:
                manongsan_instance = Nongsan.objects.get(idnongsan=idnongsan)
            except Nongsan.DoesNotExist:
                messages.error(request, 'Không tìm thấy nông sản.')
                return redirect('tonkho')

            try:
                makho_instance = Kho.objects.get(idkho=idkho)
            except Kho.DoesNotExist:
                messages.error(request, 'Không tìm thấy kho.')
                return redirect('tonkho')

            # Kiểm tra định dạng ngày
            if not parse_date(ngaynhapvao):
                messages.error(request, 'Định dạng ngày nhập vào không hợp lệ. Phải là YYYY-MM-DD.')
                return redirect('tonkho')
            if not parse_date(ngayhethan):
                messages.error(request, 'Định dạng ngày hết hạn không hợp lệ. Phải là YYYY-MM-DD.')
                return redirect('tonkho')

            tonkhoid = f"Tk-{str(uuid.uuid4())[:5]}"
            Tonkho.objects.create(
                idtonkho=tonkhoid,
                idnongsan=manongsan_instance,
                idkho=makho_instance,
                soluong=soluong,
                ngaynhapvao=ngaynhapvao,
                ngayhethan=ngayhethan,
            )
            messages.success(request, 'Tồn kho mới đã được thêm thành công.')
            return redirect('tonkho')

        elif action == "editTK" and idtonkho:
            try:
                tonkho = get_object_or_404(Tonkho, idtonkho=idtonkho)
                manongsan_instance = get_object_or_404(Nongsan, idnongsan=request.POST.get('idnongsan'))
                makho_instance = get_object_or_404(Kho, idkho=request.POST.get('idkho'))
                
                # Kiểm tra định dạng ngày
                ngaynhapvao = request.POST.get('ngaynhapvao')
                ngayhethan = request.POST.get('ngayhethan')

                if not parse_date(ngaynhapvao):
                    messages.error(request, 'Định dạng ngày nhập vào không hợp lệ. Phải là YYYY-MM-DD.')
                    return redirect('tonkho')
                if not parse_date(ngayhethan):
                    messages.error(request, 'Định dạng ngày hết hạn không hợp lệ. Phải là YYYY-MM-DD.')
                    return redirect('tonkho')

                tonkho.idnongsan = manongsan_instance
                tonkho.idkho = makho_instance
                tonkho.soluong = request.POST.get('soluong')
                tonkho.ngaynhapvao = ngaynhapvao
                tonkho.ngayhethan = ngayhethan
                tonkho.save()
                messages.success(request, 'Thông tin tồn kho đã được cập nhật thành công.')
                return redirect('tonkho')
            except Tonkho.DoesNotExist:
                messages.error(request, 'Không tìm thấy tồn kho.')
                return redirect('tonkho')
            except Nongsan.DoesNotExist:
                messages.error(request, 'Không tìm thấy nông sản.')
                return redirect('tonkho')
            except Kho.DoesNotExist:
                messages.error(request, 'Không tìm thấy kho.')
                return redirect('tonkho')

    return redirect('tonkho')

def notify_low_stock(request, tonkho_instance):
    gioihan_default = 10  # Giới hạn số lượng mặc định (số lượng còn dưới giới hạn này sẽ hiển thị thông báo)
    if tonkho_instance.soluong <= gioihan_default:
        messages.warning(request, f'Sản phẩm {tonkho_instance.idnongsan} sắp hết hàng. Số lượng còn lại: {tonkho_instance.soluong}.')

def nhacungcap(request, manhacungcap=None):
    if request.session.get('user_role') != 'admin':
        return redirect('/login/') 
    if request.method == 'GET':
        url = request.GET.get('url')
        if url == "deleteNCC" and manhacungcap:
            try:
                nhacungcap_instance = get_object_or_404(Nhacungcap, manhacungcap=manhacungcap)
                nhacungcap_instance.delete()
                messages.success(request, 'Nhà cung cấp đã được xóa thành công.')
                return redirect('nhacungcap')
            except Nhacungcap.DoesNotExist:
                messages.error(request, 'Không tìm thấy nhà cung cấp.')
                return redirect('nhacungcap')

        nhacungcaps = Nhacungcap.objects.all()
        nongsans = Nongsan.objects.all()
        return render(request, 'admin/nhacungcap.html', {'nhacungcaps': nhacungcaps, 'nongsans':nongsans})

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == "insertNCC":
            tennhacungcap = request.POST.get('tennhacungcap')
            diachi = request.POST.get('diachi')
            email = request.POST.get('email')
            sdt = request.POST.get('sdt')
            nongsanid = request.POST.get('nongsanid')

            try:
                manongsan_instance = Nongsan.objects.get(idnongsan=nongsanid)
            except Nongsan.DoesNotExist:
                messages.error(request, 'Không tìm thấy nông sản.')
                return redirect('nhacungcap')

            nhacungcapid = f"NCC-{str(uuid.uuid4())[:5]}"
            Nhacungcap.objects.create(
                manhacungcap=nhacungcapid,
                tennhacungcap=tennhacungcap,
                diachi=diachi,
                email=email,
                sdt=sdt,
                nongsanid=manongsan_instance,
            )
            messages.success(request, 'Nhà cung cấp mới đã được thêm thành công.')
            return redirect('nhacungcap')

        elif action == "editNCC" and manhacungcap:
            try:
                nhacungcap = get_object_or_404(Nhacungcap, manhacungcap=manhacungcap)
                nhacungcap.tennhacungcap = request.POST.get('tennhacungcap')
                nhacungcap.diachi = request.POST.get('diachi')
                nhacungcap.email = request.POST.get('email')
                nhacungcap.sdt = request.POST.get('sdt')

                # Gán giá trị cho manongsan_instance trước khi sử dụng
                manongsan_instance = get_object_or_404(Nongsan, idnongsan=request.POST.get('nongsanid'))
                nhacungcap.nongsanid = manongsan_instance

                nhacungcap.save()

                messages.success(request, 'Thông tin nhà cung cấp đã được cập nhật thành công.')
                return redirect('nhacungcap')
            except Nhacungcap.DoesNotExist:
                messages.error(request, 'Không tìm thấy nhà cung cấp.')
                return redirect('nhacungcap')
            except Nongsan.DoesNotExist:
                messages.error(request, 'Không tìm thấy nông sản.')
                return redirect('nhacungcap')

    return redirect('nhacungcap')


def ordernhacungcap(request, idorder=None):
    if request.session.get('user_role') != 'admin':
        return redirect('/login/') 
    if request.method == 'GET':
        url = request.GET.get('url')
        if url == "deleteOD" and idorder:
            try:
                ordernhacungcap_instance = get_object_or_404(Ordernhacungcap, idorder=idorder)
                ordernhacungcap_instance.delete()
                messages.success(request, 'Order đã được xóa thành công.')
                return redirect('ordernhacungcap')
            except Ordernhacungcap.DoesNotExist:
                messages.error(request, 'Không tìm thấy Order.')
                return redirect('ordernhacungcap')

        ordernhacungcaps = Ordernhacungcap.objects.all()
        nhacungcaps = Nhacungcap.objects.all()
        return render(request, 'admin/ordernhacungcap.html', {'ordernhacungcaps': ordernhacungcaps,'nhacungcaps':nhacungcaps})

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == "insertOD":
            nhacungcapid = request.POST.get('nhacungcapid')
            ngaygiaodich = request.POST.get('ngaygiaodich')
            loaigiaodich = request.POST.get('loaigiaodich')
            soluong = request.POST.get('soluong')
            try:
                manhacungcap_instance = Nhacungcap.objects.get(manhacungcap=nhacungcapid)
            except Nhacungcap.DoesNotExist:
                messages.error(request, 'Không tìm thấy mã nhà cng cấp.')
                return redirect('ordernhacungcap')

            # Kiểm tra định dạng ngày
            if not parse_date(ngaygiaodich):
                messages.error(request, 'Định dạng ngày nhập vào không hợp lệ. Phải là YYYY-MM-DD.')
                return redirect('ordernhacungcap')

           
            
            orderid = f"OD-{str(uuid.uuid4())[:5]}"
            Ordernhacungcap.objects.create(
                idorder=orderid,
                nhacungcapid=manhacungcap_instance,
                ngaygiaodich=ngaygiaodich,
                loaigiaodich=loaigiaodich,
                soluong=soluong,
            )
            messages.success(request, 'Order mới đã được thêm thành công.')
            return redirect('ordernhacungcap')

        elif action == "editOD" and idorder:
            try:
                ordernhacungcap = get_object_or_404(Ordernhacungcap, idorder=idorder)
                manhacungcap_instance = get_object_or_404(Nhacungcap, manhacungcap=request.POST.get('nhacungcapid'))
                
                
                # Kiểm tra định dạng ngày
                ngaygiaodich = request.POST.get('ngaygiaodich')
                
                if not parse_date(ngaygiaodich):
                    messages.error(request, 'Định dạng ngày nhập vào không hợp lệ. Phải là YYYY-MM-DD.')
                    return redirect('ordernhacungcap')

                ordernhacungcap.nhacungcapid = manhacungcap_instance
                ordernhacungcap.ngaygiaodich = ngaygiaodich
                ordernhacungcap.loaigiaodich = request.POST.get('loaigiaodich')
                ordernhacungcap.soluong = request.POST.get('soluong')
                ordernhacungcap.save()
                messages.success(request, 'Thông tin order đã được cập nhật thành công.')
                return redirect('ordernhacungcap')
            except Ordernhacungcap.DoesNotExist:
                messages.error(request, 'Không tìm thấy Order.')
                return redirect('ordernhacungcap')
            except Nhacungcap.DoesNotExist:
                messages.error(request, 'Không tìm thấy Mã nhà cung cấp.')
                return redirect('ordernhacungcap')

    return redirect('ordernhacungcap')

def account(request, idtaikhoan=None):
    if request.session.get('user_role') != 'admin':
        return redirect('/login/') 
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
    if request.session.get('user_role') != 'admin':
        return redirect('/login/') 
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
        taikhoans = Taikhoan.objects.all()
        return render(request, 'admin/nguoidung.html', {'users': users,'taikhoans': taikhoans})

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
                nguoidung.email = request.POST.get('email')
                nguoidung.phone = request.POST.get('phone')
                nguoidung.diachi = request.POST.get('address')
                nguoidung.image = request.POST.get('Image')
                nguoidung.idtaikhoan = taikhoan_instance
                nguoidung.save()
                messages.success(request, 'Thông tin người dùng đã được cập nhật thành công.')
                return redirect('nguoidung')
            except Nguoidung.DoesNotExist:
                messages.error(request, 'Không tìm thấy người dùng.')
                return redirect('nguoidung')
            except Taikhoan.DoesNotExist:
                messages.error(request, 'Không tìm thấy tài khoản.')
                return redirect('nguoidung')

    return redirect('nguoidung')
