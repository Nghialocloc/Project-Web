from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SinhVien, GiangVien
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
        fields = ( 'idsinhvien','tensinhvien', 'diachi', 'sdt', 'id',)

