from AppGiay.models import SinhVien, GiangVien
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        if(user.is_teacher):
            giangvien = GiangVien.objects.get(id= user.id)
            token['idgiangvien'] = giangvien.idgiangvien
            token['tengiangvien'] = giangvien.tengiangvien
        else:
            sinhvien = SinhVien.objects.get(id= user.id)
            token['idsinhvien'] = sinhvien.idsinhvien
            token['tensinhvien'] = sinhvien.tensinhvien
        
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer