from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Chitietdonhang,ChitiethoadonNhapHang,HoadonNhapHang,Donhang
from .models import Danhmucgiay,Chitietgiay,Khachhang,TaikhoanKhachhang,Reviewsanpham
User = get_user_model()



class UserAccountSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'tennhanvien', 'tenchucvu', 'gioitinh', 'ngaysinh', 'date_joined', 'is_manager',) 

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
        fields = ('iddonhang', 'idgiay', 'soluong', 'dongia',)

class ChitietHDNHSerializer (serializers.ModelSerializer):
    class Meta:
        model = ChitiethoadonNhapHang
        fields = ( 'iddonhang', 'idgiay', 'soluong', 'dongia',) 

class DonHangSerializer (serializers.ModelSerializer):
    class Meta:
        model = Donhang
        fields = ( 'iddonhang', 'idkhachhang', 'sotienthanhtoan', 'createday', 'confirmby', 'trangthai', 'dvvanchuyen', 'tennv_vanchuyen', 'sdt', 'socccd', 'thoigiannhan',) 

class HDNhapHangSerializer (serializers.ModelSerializer):
    class Meta:
        model = HoadonNhapHang
        fields = ( 'iddonhang', 'idkhachhang', 'sotienthanhtoan', 'createday', 'createby',)

class KhachhangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Khachhang
        fields = ( 'idkhachhang','tenkhachhang', 'diachi', 'email', 'sdt',)

class TaiKhoanKGSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaikhoanKhachhang
        fields = ( 'idtaikhoan','idkhachhang', 'username', 'password', 'gioitinh', 'ngaysinh', 'diemtichluy', 'ngaylaptk',)

class ReviewSPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviewsanpham
        fields = ( 'idtaikhoan','idloaigiay', 'comment',)

