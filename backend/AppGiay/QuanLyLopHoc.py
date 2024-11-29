from rest_framework import generics, permissions, status, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SinhVien, GiangVien
from .models import UserAccount, UserAccountManager
from .models import LopHoc, ThanhVienLop
from .serializers import UserAccountSerializer
from .serializers import SinhVienSerializer, GiangVienSerializer
from .serializers import LopHocSerializer, ThanhVienLopSerializer
from django.contrib.auth import get_user_model
import traceback
import random, string
import datetime

User = get_user_model()

# Create your views here.
def is_valid_param(param) :
    return param != " " and param is not None and param != ""


def id_generator (size = 5, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class ManageClass(APIView):

    permission_classes = (permissions.AllowAny, )

    
