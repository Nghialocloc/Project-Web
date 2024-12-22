from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import datetime
from django.utils import timezone

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
    def create_student(self, email, accountname, sex, brithday, joined, password = None):
        if not email:
            raise ValueError('User must have email address')
        
        email = self.normalize_email(email)
        user = self.model(email = email, accountname = accountname, gioitinh = sex, ngaysinh = brithday, date_joined =joined)
        
        user.set_password(password)
        user.save()
        
        return user
    
    def create_teacher(self, email, accountname, sex, brithday, joined,password = None):
        user = self.create_student(email, accountname, sex, brithday, joined, password)
        user.is_teacher = True
        
        user.save()

        return user
    
    def create_superuser(self, email, accountname, sex, brithday, joined,password = None):
        user = self.create_student(self, email, accountname,sex, brithday, joined,password)
        
        user.is_superuser = True
        user.is_staff = True
        user.is_teacher = True
        
        user.save()
        
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(db_column='IDUser', primary_key=True) # Field name made lowercase.
    email = models.EmailField(db_column='Email', max_length=120, unique= True)  # Field name made lowercase.
    accountname = models.CharField( max_length=100, unique= True, default= "Guest" ) # Field name made lowercase.
    gioitinh = models.SmallIntegerField(db_column='GioiTinh', db_comment=' Nam = 0, Nữ = 1, Khac = 2')  # Field name made lowercase.
    ngaysinh = models.DateField(db_column='NgaySinh')  # Field name made lowercase.
    date_joined = models.DateTimeField()
    is_active = models.BooleanField(default= True)
    is_teacher = models.BooleanField(default=False)
    
    objects = UserAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['accountname']
    
    def get_full_name(self):
        return self.accountname
    
    def get_short_name(self):
        return self.accountname
    
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
class GiangVien(models.Model):
    idgiangvien = models.AutoField(db_column='IDGiangVien', primary_key=True)  # Field name made lowercase.
    tengiangvien = models.CharField(db_column='TenGiangVien', max_length=50)  # Field name made lowercase.
    tenchucvu = models.CharField(db_column='TenChucVu', max_length=25)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=200)  # Field name made lowercase.
    sdt = models.CharField(db_column='SDT', max_length=15, db_collation='utf8mb3_general_ci')  # Field name made lowercase.
    id = models.ForeignKey('UserAccount', on_delete = models.PROTECT, db_column='IDuser') # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'giangvien'


class SinhVien(models.Model):
    idsinhvien = models.AutoField(db_column='IDSinhVien', primary_key=True)  # Field name made lowercase.
    tensinhvien = models.CharField(db_column='TenSinhVien', max_length=50)  # Field name made lowercase.
    nganhhoc = models.CharField(db_column='NganhHoc', max_length=30)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=200)  # Field name made lowercase.
    sdt = models.CharField(db_column='SDT', max_length=15, db_collation='utf8mb3_general_ci')  # Field name made lowercase.
    id = models.ForeignKey('UserAccount', on_delete = models.PROTECT, db_column='IDuser') # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'sinhvien'


class LopHoc(models.Model):
    idlophoc = models.AutoField(db_column='IDLopHoc', primary_key=True)  # Field name made lowercase.
    tenlophoc = models.CharField(db_column='TenLopHoc', max_length=50)  # Field name made lowercase.
    mota = models.CharField(db_column='MoTa', max_length=250, blank=True, null=True)  # Field name made lowercase.
    cahoc = models.SmallIntegerField(db_column='CaHocTrongNgay', db_comment=' Ca 1 = 0, Ca 2 = 1, Ca 3 = 2, ...')  # Field name made lowercase.
    ngayhoc = models.SmallIntegerField(db_column='NgayHocTrongTuan', db_comment=' Thứ 2 = 0, Thứ 3 = 1, Thứ 4 = 2, ...')  # Field name made lowercase.
    kyhoc = models.CharField(db_column='Ky hoc', max_length=7)  # Field name made lowercase.
    maxstudent =  models.SmallIntegerField(db_column='SoSinhVienToiDa', default= 100)  # Field name made lowercase.
    trangthai = models.SmallIntegerField(db_column='TrangThai', db_comment=' Đang đăng ký = 0, Đang hoạt động = 1, Đã kết thúc = 2')  # Field name made lowercase.
    start_day = models.DateField(db_column='NgayBatDau')  # Field name made lowercase.
    end_day = models.DateField(db_column='NgayKetThuc')  # Field name made lowercase.
    idgiangvien = models.ForeignKey('GiangVien',on_delete = models.CASCADE, db_column='IDGiangVien') # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'lophoc'


class ThanhVienLop(models.Model):
    idthanhvien = models.AutoField(db_column='IDThanhVien', primary_key=True)  # Field name made lowercase.
    tinhtranghoc = models.SmallIntegerField(db_column='TinhTrangHoc', db_comment='Đang xét duyệt = 0, Đang học  = 1, Tạm hoãn  = 2, Đã học = 3')  # Field name made lowercase.
    idsinhvien = models.ForeignKey('SinhVien', on_delete = models.CASCADE, db_column='IDSinhVien') # Field name made lowercase.
    idlophoc = models.ForeignKey('LopHoc', on_delete = models.CASCADE, db_column='IDLopHoc') # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'thanhvienlop'


class DonXinNghi(models.Model):
    iddon = models.AutoField(db_column='IDDon', primary_key=True)  # Field name made lowercase.
    idthanhvien = models.ForeignKey('ThanhVienLop', models.CASCADE, db_column='IDThanhVien') # Field name made lowercase.
    ngayxinnghi = models.DateField(db_column='NgayXinNghi') # Field name made lowercase.
    lydo = models.CharField(db_column='Lydo', max_length=300)  # Field name made lowercase.
    trangthai = models.SmallIntegerField(db_column='TrangThai', db_comment=' Đang xét duyệt = 0, Chấp nhập = 1, Từ chối = 2')  # Field name made lowercase.
    thoigiangui = models.DateTimeField(db_column='ThoigianGui') # Field name made lowercase.
    thoigianphanhoi = models.DateTimeField(db_column='ThoigianPhanhoi', blank= True, null= True) # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'donxinnghi'


class  BuoiHoc(models.Model):
    idbuoihoc = models.AutoField(db_column='IDbuoiHoc', primary_key=True)  # Field name made lowercase.
    idlophoc = models.ForeignKey('LopHoc', models.CASCADE, db_column='IDLopHoc') # Field name made lowercase.
    ngaydienra = models.DateField(db_column='NgayDienRa') # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'buoihoc'


class DiemDanh(models.Model):
    iddiemdanh = models.AutoField(db_column='IDDiemDanh', primary_key=True)  # Field name made lowercase.
    idbuoihoc = models.ForeignKey('BuoiHoc', models.CASCADE, db_column='IDBuoiHoc') # Field name made lowercase.
    idsinhvien = models.ForeignKey('SinhVien', models.CASCADE, db_column='IDSinhVien') # Field name made lowercase.
    trangthaidiemdanh = models.SmallIntegerField(db_column='TrangThaiDiemDanh', db_comment=' Có mặt = 0, Muộn học = 1, Vắng có phép = 2, Vắng không có phép = 3')  # Field name made lowercase.
    thoigiandiemdanh = models.DateTimeField(db_column='ThoigianDiemDanh') # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'diemdanh'


class TaiLieuHocTap(models.Model):
    idtailieu = models.IntegerField(db_column='IDTaiLieu', primary_key=True) # Field name made lowercase.
    idlophoc = models.ForeignKey('LopHoc', models.CASCADE, db_column='IDLopHoc') # Field name made lowercase.
    tentailieu = models.CharField(db_column='TenTaiLieu', max_length=100) # Field name made lowercase.
    description = models.CharField(db_column='Descriptions', max_length=200, null=True) # Field name made lowercase.
    loaitailieu = models.SmallIntegerField(db_column='LoaiTaiLieu', db_comment=' Bài giảng = 0, Bài làm thêm = 1, Video hướng dẫn = 2')  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=255) # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tailieu'


class BaiTap(models.Model):
    idbaitap = models.IntegerField(db_column='IDBaiTap', primary_key=True)  # ID bài tập
    idlophoc = models.ForeignKey('LopHoc', on_delete=models.CASCADE, db_column='IDLopHoc')  # Liên kết lớp học
    tenbaitap = models.CharField(max_length=50) # Tên bài tập
    mota = models.CharField(db_column='MoTa', max_length=200)  # Mô tả chi tiết bài tập
    filebaitap = models.FileField(db_column='FileBaiTap', upload_to='baitap_files/')  # File đính kèm bài tập
    deadline = models.DateTimeField(db_column='HanHop') # Hạn nộp bài tập
    create_day = models.DateTimeField(db_column='NgayTao') # Ngày tạo bài tập

    class Meta:
        managed = True
        db_table = 'baitap'


class BaiLam(models.Model):
    idbailam = models.IntegerField(db_column='IDBaiLam', primary_key=True)  # ID nộp bài
    idbaitap = models.ForeignKey('BaiTap', on_delete=models.CASCADE, db_column='IDBaiTap') # Liên kết tới bài tập
    idsinhvien = models.ForeignKey('SinhVien', on_delete=models.CASCADE, db_column='IDSinhVien')  # Liên kết sinh viên
    filebailam = models.FileField(db_column='FileBaiLam', upload_to='bailam_files/') # File bài giải sinh viên nộp
    description = models.CharField(db_column='MoTa', max_length = 200,null=True, blank=True) # Mô tả bài làm (nếu không có file)
    ngaynop = models.DateTimeField(db_column='NgayNop') # Ngày nộp bài
    diem = models.FloatField(db_column='DiemSo', null=True, blank=True) # Điểm số bài tập (giáo viên chấm)

    class Meta:
        managed = True
        db_table = 'bailam'


class ThongbBaoTinNhan(models.Model):
    message_id = models.CharField(primary_key=True, max_length=8, db_column='IDMessage')
    sender_id = models.ForeignKey('UserAccount', on_delete = models.PROTECT, db_column='IDSender') # Field name made lowercase.
    receiver_id = models.IntegerField(db_column='IDReceiver')
    message = models.CharField(db_column='NoiDung', max_length=200)
    type = models.SmallIntegerField(db_column='LoaiTinNhan', db_comment='Don nghi hoc = 0, Diểm bài kiểm tra = 1, Ket qua xet đơn nghỉ = 2, Bai tap moi = 3')  # Field name made lowercase.
    related_id = models.IntegerField(db_column='IDLienHe', blank=True, null=True)
    is_read = models.BooleanField(db_column='DaDoc')

    class Meta:
        managed = True
        db_table = 'thongbao'