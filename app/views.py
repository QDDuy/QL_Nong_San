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

def shop_detail(request,idnongsan):
    nongsan=get_object_or_404(Nongsan,idnongsan=idnongsan)
    
    return render(request, 'user/shop-detail.html',{'nongsan':nongsan})
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
    user_id = request.session.get('manguoidung')
    
    if user_id:
        user = get_object_or_404(Nguoidung, manguoidung=user_id)
    else:
        return redirect('login')  # Replace 'login' with your actual login URL name

    nongsan = get_object_or_404(Nongsan, idnongsan=product_id)
    
    quantity = 1
    cart_id = f"C_{uuid.uuid4()}"
    cart_item, created = Cart.objects.get_or_create(
        cart_id=cart_id, 
        user=user,
        nongsan=nongsan,
        quantity=quantity
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, f'{nongsan.ten} has been added to your cart.')

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

def nongsan(request, IdNongSan=None):
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



