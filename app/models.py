from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Danhmuc(models.Model):
    madanhmuc = models.CharField(db_column='MaDanhMuc', primary_key=True, max_length=50)  # Field name made lowercase.
    tendanhmuc = models.CharField(db_column='TenDanhMuc', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'danhmuc'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Donhang(models.Model):
    madonhang = models.CharField(db_column='MaDonHang', primary_key=True, max_length=50)  # Field name made lowercase.
    manguoidung = models.ForeignKey('Nguoidung', models.DO_NOTHING, db_column='MaNguoiDung', blank=True, null=True)  # Field name made lowercase.
    tonggia = models.DecimalField(db_column='TongGia', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ngaydat = models.DateField(db_column='NgayDat', blank=True, null=True)  # Field name made lowercase.
    trangthai = models.CharField(db_column='TrangThai', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'donhang'


class Giamgia(models.Model):
    magiamgia = models.CharField(db_column='MaGiamGia', primary_key=True, max_length=50)  # Field name made lowercase.
    idnongsan = models.ForeignKey('Nongsan', models.DO_NOTHING, db_column='IdNongSan', blank=True, null=True)  # Field name made lowercase.
    phantramgiam = models.DecimalField(db_column='PhanTramGiam', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ngaybatdau = models.DateField(db_column='NgayBatDau', blank=True, null=True)  # Field name made lowercase.
    ngayketthuc = models.DateField(db_column='NgayKetThuc', blank=True, null=True)  # Field name made lowercase.
    mota = models.TextField(db_column='MoTa', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'giamgia'


class Kho(models.Model):
    idkho = models.CharField(db_column='IdKho', primary_key=True, max_length=50)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'kho'


class Nguoidung(models.Model):
    manguoidung = models.CharField(db_column='MaNguoiDung', primary_key=True, max_length=50)  # Field name made lowercase.
    hovaten = models.CharField(db_column='HoVaTen', max_length=100, blank=True, null=True)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    idtaikhoan = models.ForeignKey('Taikhoan', models.DO_NOTHING, db_column='IdTaiKhoan', blank=True, null=True)  # Field name made lowercase.
    image=models.ImageField(upload_to='nguoidung',null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'nguoidung'
  
class Nhacungcap(models.Model):
    manhacungcap = models.CharField(db_column='MaNhaCungCap', primary_key=True, max_length=50)  # Field name made lowercase.
    tennhacungcap = models.CharField(db_column='TenNhaCungCap', max_length=100, blank=True, null=True)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sdt = models.CharField(db_column='SDT', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nongsanid = models.ForeignKey('Nongsan', models.DO_NOTHING, db_column='NongSanId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nhacungcap'


class Nhanvien(models.Model):
    manhanvien = models.CharField(db_column='MaNhanVien', primary_key=True, max_length=50)  # Field name made lowercase.
    tennhanvien = models.CharField(db_column='TenNhanVien', max_length=100, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sodienthoai = models.CharField(db_column='SoDienThoai', max_length=20, blank=True, null=True)  # Field name made lowercase.
    luong = models.DecimalField(db_column='Luong', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    calamviec = models.CharField(db_column='CaLamViec', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idtaikhoan = models.ForeignKey('Taikhoan', models.DO_NOTHING, db_column='IdTaiKhoan', blank=True, null=True)  # Field name made lowercase.
    image=models.ImageField(upload_to='nhanvien/',null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'nhanvien'


class Nongsan(models.Model):
    idnongsan = models.CharField(db_column='IdNongSan', primary_key=True, max_length=50)  # Field name made lowercase.
    ten = models.CharField(db_column='Ten', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mota = models.TextField(db_column='MoTa', blank=True, null=True)  # Field name made lowercase.
    gia = models.DecimalField(db_column='Gia', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    trongluong = models.DecimalField(db_column='TrongLuong', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    madanhmuc = models.ForeignKey(Danhmuc, models.DO_NOTHING, db_column='MaDanhMuc', blank=True, null=True)  # Field name made lowercase.
    image=models.ImageField(upload_to='nongsan/',null=True, blank=True )
    class Meta:
        managed = False
        db_table = 'nongsan'

class DonHangDetail(models.Model):
        ma_donhang_detail = models.CharField(max_length=255, primary_key=True,db_column='MaDonHangDetail')
        ma_donhang = models.ForeignKey(Donhang, on_delete=models.CASCADE, db_column='MaDonHang')
        id_nongsan = models.ForeignKey(Nongsan, on_delete=models.CASCADE, db_column='IdNongSan')
        quantity = models.IntegerField()

        def __str__(self):
            return self.ma_donhang_detail
        class Meta:
            managed = False
            db_table = 'donhang_detail'
class Cart(models.Model):
    cart_id = models.CharField(primary_key=True, max_length=255)
    user = models.ForeignKey('Nguoidung', models.DO_NOTHING)
    nongsan = models.ForeignKey('Nongsan', models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cart'

class Ordernhacungcap(models.Model):
    idorder = models.CharField(db_column='IdOrder', primary_key=True, max_length=50)  # Field name made lowercase.
    nhacungcapid = models.ForeignKey(Nhacungcap, models.DO_NOTHING, db_column='NhaCungCapId', blank=True, null=True)  # Field name made lowercase.
    ngaygiaodich = models.DateField(db_column='NgayGiaoDich', blank=True, null=True)  # Field name made lowercase.
    loaigiaodich = models.CharField(db_column='LoaiGiaoDich', max_length=255, blank=True, null=True)  # Field name made lowercase.
    soluong = models.IntegerField(db_column='SoLuong', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ordernhacungcap'


class Taikhoan(models.Model):
    idtaikhoan = models.CharField(db_column='IdTaiKhoan', primary_key=True, max_length=50)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=50, blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'taikhoan'
   


class Tonkho(models.Model):
    idtonkho = models.CharField(db_column='IdTonKho', primary_key=True, max_length=50)  # Field name made lowercase.
    idnongsan = models.ForeignKey(Nongsan, models.DO_NOTHING, db_column='IdNongSan', blank=True, null=True)  # Field name made lowercase.
    idkho = models.ForeignKey(Kho, models.DO_NOTHING, db_column='IdKho', blank=True, null=True)  # Field name made lowercase.
    soluong = models.IntegerField(db_column='SoLuong', blank=True, null=True)  # Field name made lowercase.
    ngaynhapvao = models.DateField(db_column='NgayNhapVao', blank=True, null=True)  # Field name made lowercase.
    ngayhethan = models.DateField(db_column='NgayHetHan', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tonkho'