from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import datetime

# Create your models here.

#AuthGroup
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


#Account Managerclass
class UserAccountManager(BaseUserManager):
    def create_user(self, email, fullName, role, sex, brithday, joined,password = None):
        if not email:
            raise ValueError('User must have email address')
        
        email = self.normalize_email(email)
        user = self.model(email = email, tennhanvien = fullName, tenchucvu = role, gioitinh = sex, ngaysinh = brithday, date_joined =joined)
        
        user.set_password(password)
        user.save()
        
        return user
    
    def create_manager(self, email, fullName, role, sex, brithday, joined,password = None):
        user = self.create_user(self, email, fullName, role, sex, brithday, joined,password)
        user.is_manager = True
        
        user.save()

        return user
    def create_superuser(self, email, fullName, role, sex, brithday, joined,password = None):
        user = self.create_user(self, email, fullName, role, sex, brithday, joined,password)
        
        user.is_superuser = True
        user.is_staff = True
        user.is_manager = True
        
        user.save()
        
        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(db_column='IDUser', primary_key=True) # Field name made lowercase.
    email = models.EmailField( max_length=254, unique= True ) # Field name made lowercase.
    tennhanvien = models.CharField(db_column='TenNhanVien', max_length=50)  # Field name made lowercase.
    tenchucvu = models.CharField(db_column='ChucVu', max_length=50)  # Field name made lowercase.
    gioitinh = models.SmallIntegerField(db_column='GioiTinh', db_comment=' Nam = 0,Nữ = 1, Khac = 2')  # Field name made lowercase.
    ngaysinh = models.DateField(db_column='NgaySinh')  # Field name made lowercase.
    date_joined = models.DateTimeField()
    is_active = models.BooleanField(default= True)
    is_manager = models.BooleanField(default=False)
    
    objects = UserAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullName']
    
    def get_full_name(self):
        return self.tennhanvien
    
    def get_short_name(self):
        return self.tennhanvien 
    
    def __str__(self):
        return self.email
    

#DjangoGroup
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

#DatabaseGroup
class Danhmucgiay(models.Model):
    iddanhmuc = models.AutoField(db_column='IDDanhMuc', primary_key=True)  # Field name made lowercase.
    tendanhmuc = models.CharField(db_column='TenDanhMuc', max_length=100)  # Field name made lowercase.
    loaigiay = models.CharField(db_column='LoaiGiay', max_length=50)  # Field name made lowercase.
    hangsanxuat = models.CharField(db_column='HangSanXuat', max_length=50)  # Field name made lowercase.
    giatien = models.IntegerField(db_column='GiaTien')  # Field name made lowercase.
    doituong = models.SmallIntegerField(db_column='DoiTuong', db_comment='Đối tượng hướng tới : Nam = 0,Nữ = 1, Khac = 2')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'danhmucgiay'



class Chitietgiay(models.Model):
    idgiay = models.AutoField(db_column='IDGiay', primary_key=True, db_comment='Mã của mặt hàng giầy')  # Field name made lowercase.
    iddanhmuc = models.ForeignKey('Danhmucgiay', models.DO_NOTHING, db_column='IDDanhMuc')  # Field name made lowercase.
    kichco = models.FloatField(db_column='KichCo')  # Field name made lowercase.
    mausac = models.CharField(db_column='MauSac', max_length=20)  # Field name made lowercase.
    sotonkho = models.IntegerField(db_column='SoTonKho')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chitietgiay'


class Chitietdonhang(models.Model):
    iddonhang = models.ForeignKey('Donhang', models.DO_NOTHING, db_column='IDDonHang')  # Field name made lowercase.
    idgiay = models.ForeignKey('Chitietgiay', models.DO_NOTHING, db_column='IDGiay')  # Field name made lowercase.
    soluong = models.SmallIntegerField(db_column='SoLuong')  # Field name made lowercase.
    dongia = models.IntegerField(db_column='DonGia')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chitietdonhang'


class ChitiethoadonNhapHang(models.Model):
    idhoadon = models.ForeignKey('HoadonNhapHang', models.DO_NOTHING, db_column='IDHoaDon')  # Field name made lowercase.
    idgiay = models.ForeignKey(Chitietgiay, models.DO_NOTHING, db_column='IDGiay')  # Field name made lowercase.
    soluong = models.SmallIntegerField(db_column='SoLuong')  # Field name made lowercase.
    dongia = models.IntegerField(db_column='DonGia')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chitiethoadon_nhap_hang'


class Donhang(models.Model):
    iddonhang = models.AutoField(db_column='IDDonHang', primary_key=True)  # Field name made lowercase.
    idkhachhang = models.ForeignKey('Khachhang', models.DO_NOTHING, db_column='IDKhachHang')  # Field name made lowercase.
    sotienthanhtoan = models.IntegerField(db_column='SoTienThanhToan')  # Field name made lowercase.
    createday = models.DateField(db_column='CreateDay')  # Field name made lowercase.
    createby = models.CharField(db_column='CreateBy', max_length=50)  # Field name made lowercase.
    trangthai = models.SmallIntegerField(db_column='TrangThai', db_comment='Trạng thái đon hàng : Checking=0, Confirm=1, Đang giao=2, Đã hoàn thành=3') 
 # Field name made lowercase.
    dvvanchuyen = models.CharField(db_column='DVVanChuyen', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tennv_vanchuyen = models.CharField(db_column='TenNV_VanChuyen', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sdt = models.CharField(db_column='SDT', max_length=15, blank=True, null=True)  # Field name made lowercase.
    socccd = models.CharField(db_column='SoCCCD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    thoigiannhan = models.DateTimeField(db_column='ThoiGianNhan', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'donhang'


class HoadonNhapHang(models.Model):
    idhoadon = models.AutoField(db_column='IDHoaDon', primary_key=True)  # Field name made lowercase.
    idkhachhang = models.ForeignKey('Khachhang', models.DO_NOTHING, db_column='IDKhachHang')  # Field name made lowercase.
    sotienthanhtoan = models.IntegerField(db_column='SoTienThanhToan')  # Field name made lowercase.
    createday = models.DateField(db_column='CreateDay')  # Field name made lowercase.
    createby = models.CharField(db_column='CreateBy', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hoadon_nhap_hang'


class Khachhang(models.Model):
    idkhachhang = models.AutoField(db_column='IDKhachHang', primary_key=True)  # Field name made lowercase.
    tenkhachhang = models.CharField(db_column='TenKhachHang', max_length=50)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=200)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100)  # Field name made lowercase.
    sdt = models.CharField(db_column='SDT', max_length=15, db_collation='utf8mb3_general_ci')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'khachhang'


class TaikhoanKhachhang(models.Model):
    idtaikhoan = models.AutoField(db_column='IDTaiKhoan', primary_key=True)  # Field name made lowercase.
    idkhachhang = models.CharField(db_column='IDKhachHang', max_length=255)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=30)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=30)  # Field name made lowercase.
    gioitinh = models.SmallIntegerField(db_column='GioiTinh', db_comment=' Nam = 0,Nữ = 1, Khac = 2')  # Field name made lowercase.
    ngaysinh = models.DateField(db_column='NgaySinh')  # Field name made lowercase.
    diemtichluy = models.IntegerField(db_column='DiemTichLuy')  # Field name made lowercase.
    ngaylaptk = models.DateField(db_column='NgayLapTK')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'taikhoan_khachhang'


class Reviewsanpham(models.Model):
    idtaikhoan = models.ForeignKey('TaikhoanKhachhang', models.DO_NOTHING, db_column='IDTaiKhoan')  # Field name made lowercase.
    idloaigiay = models.ForeignKey(Chitietgiay, models.DO_NOTHING, db_column='IDLoaiGiay')  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=300)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'reviewsanpham'


