from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Chitietdonhang,ChitiethoadonNhapHang,HoadonNhapHang,Donhang
from .models import Danhmucgiay,Chitietgiay,Khachhang,Nhanvien,Reviewsanpham
User = get_user_model()



class DanhMucGiaySerializer (serializers.ModelSerializer):
    class Meta:
        model = Danhmucgiay
        fields = ('iddanhmuc','tendanhmuc', 'loaigiay', 'hangsanxuat','giatien', 'doituong') 

class ChitietGiaySerializer (serializers.ModelSerializer):
    class Meta:
        model = Chitietgiay
        fields = ('idgiay', 'iddanhmuc', 'kichco', 'mausac','sotonkho',) 

class ChitietDHSerializer (serializers.ModelSerializer):
    class Meta:
        model = Chitietdonhang
        fields = ('idchitiet','iddonhang', 'idgiay', 'soluong', 'dongia',)

class ChitietHDNHSerializer (serializers.ModelSerializer):
    class Meta:
        model = ChitiethoadonNhapHang
        fields = ('idchitiet','iddonhang', 'idgiay', 'soluong', 'dongia',)

class DonHangSerializer (serializers.ModelSerializer):
    class Meta:
        model = Donhang
        fields = ( 'iddonhang', 'idkhachhang', 'sotienthanhtoan', 'createday', 'confirmby', 'trangthai', 'dvvanchuyen', 'tennv_vanchuyen', 'sdt', 'socccd', 'thoigiannhan',) 

class HDNhapHangSerializer (serializers.ModelSerializer):
    class Meta:
        model = HoadonNhapHang
        fields = ( 'iddonhang', 'idkhachhang', 'sotienthanhtoan', 'createday', 'createby',)

class UserAccountSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email','accountname', 'gioitinh', 'ngaysinh', 'date_joined', 'is_manager',)

class NhanvienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nhanvien
        fields = ( 'idnhanvien','tennhanvien', 'tenchucvu', 'diachi', 'sdt', 'id',)

class KhachhangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Khachhang
        fields = ( 'idkhachhang','tenkhachhang', 'diachi', 'email', 'sdt', 'id','diemtichluy')

class ReviewSPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviewsanpham
        fields = ( 'idreview','id','idloaigiay', 'comment', 'createday')

