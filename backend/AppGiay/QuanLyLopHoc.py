from rest_framework import generics, permissions, status, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
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


class ManageClassTeacher(APIView):

    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        try:
            user = request.user
            if not user.is_teacher:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = LopHocSerializer(data=request.data)
            giangvien = serializer.data.get('idgiangvien')
            if GiangVien.objects.filter(idgiangvien=giangvien).count() == 0:
                return  Response(
                        {'error': 'Khong tim thay giang vien'}, 
                        status= status.HTTP_404_NOT_FOUND
                    )
            else: 
                if serializer.is_valid():
                    while True:
                        idlophoc = id_generator(size=5)
                        if (LopHoc.objects.filter(idlophoc = idlophoc).count() == 0):
                            break                      
                    
                    tenlophoc = serializer.data.get('tenlophoc') 
                    mota = serializer.data.get('mota')
                    cahoc = serializer.data.get('cahoc')

                
                    lophoc = LopHoc(idlophoc = idlophoc, tenlophoc = tenlophoc, mota = mota, cahoc = cahoc, idgiangvien = giangvien)
                    lophoc.save()
                
                    return Response(
                        {"Da luu thong tin lop moi" : LopHocSerializer(lophoc).data},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return  Response(
                        {'error': 'Du lieu dau vao bi thieu hoac sai'}, 
                        status= status.HTTP_400_BAD_REQUEST
                    )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        try:
            list_class = []
            user = request.user
            if not user.is_teacher:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            user_id = user.data['id']
            giangvien = GiangVien.objects.get(user_id = user_id)
            giangvien_id = giangvien.idgiangvien

            lopgiangday = LopHoc.objects.filter(idgiangvien = giangvien_id)
            lopgiangday_seria = LopHocSerializer(data = lopgiangday, many = True)
            if lopgiangday_seria.is_valid():
                for group in lopgiangday_seria :
                    idlophoc = group.data.get('idlophoc')
                    tenlophoc = group.data.get('tenlophoc')
                    cahoc = group.data.get('cahoc')
                    mota = group.data.get('mota')

                    list_class.append(
                        {
                            "Ma lop" : idlophoc,
                            "Ten lop hoc" : tenlophoc,
                            "Mo ta" : mota,
                            "Gio bat dau" : cahoc
                        }
                    )

                return Response(
                    {'Danh sach lop giang day': list_class}, 
                    status= status.HTTP_200_OK
                )
            else:
                return Response(
                    {'Du lieu gap su co'}, 
                    status= status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong!'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request):
        try: 
            user= request.user
            if not user.is_teacher:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            data=request.data
            idlophoc = data['idlophoc']
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return JsonResponse(
                    {'error': 'No matching'}
                    ,safe=False 
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            idgiangvien =  data['idgiangvien']
            if GiangVien.objects.filter(idgiangvien = idgiangvien).count() == 0:
                return  Response(
                    {'error': 'Khong tim thay giang vien'}, 
                    status= status.HTTP_404_NOT_FOUND
                )
            tenlophoc = data['tenlophoc']
            cahoc = data['cahoc']
            mota = data['mota']

            lophoc = LopHoc.objects.get(idlophoc = idlophoc)
            lophoc.tenlophoc = tenlophoc
            lophoc.cahoc = cahoc
            lophoc.mota = mota
            lophoc.save()
            return JsonResponse(
                {'Update success'}
                , safe=False 
                ,status= status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        try: 
            user= request.user
            if not user.is_teacher:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data=request.data
            idlophoc = data['idlophoc']
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return JsonResponse(
                    {'error': 'No matching'}
                    ,safe=False 
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            else:
                list_thanhvien = ThanhVienLop.objects.filter(idlophoc = idlophoc)
                if list_thanhvien.count() != 0:
                    list_thanhvien_seria = ThanhVienLopSerializer(list_thanhvien, many = True)
                    for group in list_thanhvien_seria.data:
                        thanhvien = ThanhVienLop.objects.get(idthanhvien = group.get('idthanhvien'))
                        thanhvien.delete()
                lophoc = LopHoc.objects.get(idlophoc = idlophoc)
                lophoc.delete()

                return JsonResponse(
                    {'Result': 'Delete successful'}
                    ,safe=False 
                    ,status= status.HTTP_202_ACCEPTED
                )        

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class ManageClassStudent(APIView):

    permission_classes = (permissions.AllowAny, )
    
