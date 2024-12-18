from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SinhVien, GiangVien, LopHoc, ThanhVienLop, DonXinNghi, BuoiHoc, DiemDanh, TaiLieuHocTap, BaiTap, BaiLam
User = get_user_model()


class UserAccountSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email','accountname', 'gioitinh', 'ngaysinh', 'date_joined', 'is_teacher',)

class GiangVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiangVien
        fields = ( 'idgiangvien','tengiangvien', 'tenchucvu', 'diachi', 'sdt', 'id',)

class SinhVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinhVien
        fields = ( 'idsinhvien','tensinhvien', 'nganhhoc','diachi', 'sdt', 'id',)

class LopHocSerializer(serializers.ModelSerializer):
    class Meta:
        model = LopHoc
        fields = ( 'idlophoc','tenlophoc', 'mota', 'cahoc', 'ngayhoc', 'kyhoc', 'maxstudent', 'trangthai', 'start_day', 'end_day','idgiangvien',)

class ThanhVienLopSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThanhVienLop
        fields = ( 'idthanhvien','tinhtranghoc', 'idsinhvien','idlophoc',)

class DonXinNghiSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonXinNghi
        fields = ( 'iddon','idthanhvien', 'ngayxinnghi','lydo', 'trangthai', 'thoigiangui', 'thoigianphanhoi',)

class BuoiHocSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuoiHoc
        fields = ( 'idbuoihoc','idlophoc', 'ngaydienra',)

class DiemDanhSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiemDanh
        fields = ( 'iddiemdanh', 'idbuoihoc', 'idsinhvien', 'trangthaidiemdanh', 'thoigiandiemdanh',)

class TaiLieuHocTapSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaiLieuHocTap 
        fields = ['idtailieu', 'idlophoc', 'tentailieu', 'description', 'loaitailieu', 'link',]

class BaiTapSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaiTap
        fields = ('idbaitap', 'idlophoc','tenbaitap', 'mota', 'filebaitap', 'deadline', 'create_day',)

class BaiLamSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaiLam
        fields = ('idbailam', 'idbaitap', 'idsinhvien', 'filebailam', 'description', 'ngaynop', 'diem',)