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

def kho(request):
    context = {}
    return render(request, 'admin/kho.html', context)

def tonkho(request):
    context = {}
    return render(request, 'admin/tonkho.html', context)

def nhacungcap(request):
    context = {}
    return render(request, 'admin/nhacungcap.html', context)

def ordernhacungcap(request):
    context = {}
    return render(request, 'admin/ordernhacungcap.html', context)

def logout(request):
    if 'checklogin' in request.session:
        del request.session['checklogin']
    if 'customer_name' in request.session:
        del request.session['khachHang_name']
    return redirect('/')


def kho(request, idkho=None):
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

    return redirect('kho')

def tonkho(request, idtonkho=None):
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

def nhacungcap(request, manhacungcap=None):
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
        return render(request, 'admin/nhacungcap.html', {'nhacungcaps': nhacungcaps})

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
        return render(request, 'admin/ordernhacungcap.html', {'ordernhacungcaps': ordernhacungcaps})

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