from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SinhVien, GiangVien, LopHoc, ThanhVienLop
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
        fields = ( 'idlophoc','tenlophoc', 'mota', 'cahoc', 'idgiangvien',)

class ThanhVienLopSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThanhVienLop
        fields = ( 'idthanhvien','tinhtranglop', 'idsinhvien','idlophoc',)

