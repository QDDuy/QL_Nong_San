# Generated by Django 5.0.6 on 2024-06-25 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Danhmuc',
            fields=[
                ('madanhmuc', models.CharField(db_column='MaDanhMuc', max_length=50, primary_key=True, serialize=False)),
                ('tendanhmuc', models.CharField(blank=True, db_column='TenDanhMuc', max_length=100, null=True)),
            ],
            options={
                'db_table': 'danhmuc',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Donhang',
            fields=[
                ('madonhang', models.CharField(db_column='MaDonHang', max_length=50, primary_key=True, serialize=False)),
                ('tonggia', models.DecimalField(blank=True, db_column='TongGia', decimal_places=2, max_digits=15, null=True)),
                ('ngaydat', models.DateField(blank=True, db_column='NgayDat', null=True)),
                ('trangthai', models.CharField(blank=True, db_column='TrangThai', max_length=50, null=True)),
            ],
            options={
                'db_table': 'donhang',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Giamgia',
            fields=[
                ('magiamgia', models.CharField(db_column='MaGiamGia', max_length=50, primary_key=True, serialize=False)),
                ('phantramgiam', models.DecimalField(blank=True, db_column='PhanTramGiam', decimal_places=2, max_digits=5, null=True)),
                ('ngaybatdau', models.DateField(blank=True, db_column='NgayBatDau', null=True)),
                ('ngayketthuc', models.DateField(blank=True, db_column='NgayKetThuc', null=True)),
                ('mota', models.TextField(blank=True, db_column='MoTa', null=True)),
            ],
            options={
                'db_table': 'giamgia',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Kho',
            fields=[
                ('idkho', models.CharField(db_column='IdKho', max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=100, null=True)),
                ('diachi', models.CharField(blank=True, db_column='DiaChi', max_length=255, null=True)),
            ],
            options={
                'db_table': 'kho',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Nguoidung',
            fields=[
                ('manguoidung', models.CharField(db_column='MaNguoiDung', max_length=50, primary_key=True, serialize=False)),
                ('hovaten', models.CharField(blank=True, db_column='HoVaTen', max_length=100, null=True)),
                ('diachi', models.CharField(blank=True, db_column='DiaChi', max_length=255, null=True)),
                ('phone', models.CharField(blank=True, db_column='Phone', max_length=20, null=True)),
                ('email', models.CharField(blank=True, db_column='Email', max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True)),
            ],
            options={
                'db_table': 'nguoidung',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Nhacungcap',
            fields=[
                ('manhacungcap', models.CharField(db_column='MaNhaCungCap', max_length=50, primary_key=True, serialize=False)),
                ('tennhacungcap', models.CharField(blank=True, db_column='TenNhaCungCap', max_length=100, null=True)),
                ('diachi', models.CharField(blank=True, db_column='DiaChi', max_length=255, null=True)),
                ('email', models.CharField(blank=True, db_column='Email', max_length=100, null=True)),
                ('sdt', models.CharField(blank=True, db_column='SDT', max_length=20, null=True)),
            ],
            options={
                'db_table': 'nhacungcap',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Nhanvien',
            fields=[
                ('manhanvien', models.CharField(db_column='MaNhanVien', max_length=50, primary_key=True, serialize=False)),
                ('tennhanvien', models.CharField(blank=True, db_column='TenNhanVien', max_length=100, null=True)),
                ('email', models.CharField(blank=True, db_column='Email', max_length=100, null=True)),
                ('sodienthoai', models.CharField(blank=True, db_column='SoDienThoai', max_length=20, null=True)),
                ('luong', models.DecimalField(blank=True, db_column='Luong', decimal_places=2, max_digits=12, null=True)),
                ('calamviec', models.CharField(blank=True, db_column='CaLamViec', max_length=50, null=True)),
                ('image', models.ImageField(blank=True, null=True)),
            ],
            options={
                'db_table': 'nhanvien',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Nongsan',
            fields=[
                ('idnongsan', models.CharField(db_column='IdNongSan', max_length=50, primary_key=True, serialize=False)),
                ('ten', models.CharField(blank=True, db_column='Ten', max_length=100, null=True)),
                ('mota', models.TextField(blank=True, db_column='MoTa', null=True)),
                ('gia', models.DecimalField(blank=True, db_column='Gia', decimal_places=2, max_digits=15, null=True)),
                ('trongluong', models.DecimalField(blank=True, db_column='TrongLuong', decimal_places=2, max_digits=10, null=True)),
                ('image', models.ImageField(blank=True, null=True )),

            ],
            options={
                'db_table': 'nongsan',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ordernhacungcap',
            fields=[
                ('idorder', models.CharField(db_column='IdOrder', max_length=50, primary_key=True, serialize=False)),
                ('ngaygiaodich', models.DateField(blank=True, db_column='NgayGiaoDich', null=True)),
                ('loaigiaodich', models.CharField(blank=True, db_column='LoaiGiaoDich', max_length=255, null=True)),
                ('soluong', models.IntegerField(blank=True, db_column='SoLuong', null=True)),
            ],
            options={
                'db_table': 'ordernhacungcap',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Taikhoan',
            fields=[
                ('idtaikhoan', models.CharField(db_column='IdTaiKhoan', max_length=50, primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, db_column='UserName', max_length=50, null=True)),
                ('password', models.CharField(blank=True, db_column='Password', max_length=50, null=True)),
                ('role', models.CharField(blank=True, db_column='Role', max_length=50, null=True)),
            ],
            options={
                'db_table': 'taikhoan',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tonkho',
            fields=[
                ('idtonkho', models.CharField(db_column='IdTonKho', max_length=50, primary_key=True, serialize=False)),
                ('soluong', models.IntegerField(blank=True, db_column='SoLuong', null=True)),
                ('ngaynhapvao', models.DateField(blank=True, db_column='NgayNhapVao', null=True)),
                ('ngayhethan', models.DateField(blank=True, db_column='NgayHetHan', null=True)),
            ],
            options={
                'db_table': 'tonkho',
                'managed': False,
            },
        ),
    ]
