from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SinhVien, GiangVien
from .models import LopHoc, ThanhVienLop, TaiLieuHocTap
from .serializers import UserAccountSerializer, SinhVienSerializer
from .serializers import LopHocSerializer, ThanhVienLopSerializer, TaiLieuHocTapSerializer
from django.contrib.auth import get_user_model
import traceback
import random, string
import datetime

User = get_user_model()

def is_valid_param(param) :
    return param != " " and param is not None and param != ""


def id_generator (size, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class ManageMaterial(APIView):

    permission_classes = (permissions.AllowAny, )

    #Upload material
    def post(self, request, format=None):
        try:
            data = request.data
            user = request.user
            if (not user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            idlophoc = data['idlophoc'] 
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return  Response(
                    {
                        'code' : 1004,
                        'message': 'Class not found. Please check id input' 
                    }, 
                    status= status.HTTP_404_NOT_FOUND
                )
            
            tentailieu = data['tentailieu']
            description = data['description']
            loaitailieu = data['loaitailieu']
            link = data['link']

            if is_valid_param(tentailieu) == False or is_valid_param(loaitailieu) == False or is_valid_param(link):
                return  Response(
                    {
                        'code' : 1002,
                        'message': 'The material info is not complete. Please check and add all missing input' 
                    }, 
                    status= status.HTTP_404_NOT_FOUND
                )

            while True:
                idtailieu= id_generator(size=6)
                if (TaiLieuHocTap.objects.filter(idtailieu = idtailieu).count() == 0):
                    break
            
            tailieu = TaiLieuHocTap(idtailieu = idtailieu, tentailieu = tentailieu, description = description,
                                    loaitailieu = loaitailieu, link = link,)
            tailieu.save()

            return Response(
                {
                    'code': 1000,
                    'meassage': "OK"
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Get material list
    def get(self, request):
        try:
            data = request.data
            idlophoc = data['idlophoc']
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return Response(
                    {
                        'code' : 1004,
                        'message': 'Class not found. Please try again.' 
                    }
                    ,status= status.HTTP_400_BAD_REQUEST
                )      
            lophoc  = LopHoc.objects.get(idlophoc = idlophoc)
            tenlophoc = lophoc.tenlophoc

            list_material = []

            tailieu = TaiLieuHocTap.objects.filter(idlophoc = idlophoc)
            tailieu_seria = TaiLieuHocTapSerializer(tailieu, many = True)
            for group in tailieu_seria.data :
                tentailieu = group.get('tentailieu')
                description = group.get('description')
                loaitailieu = group.get('loaitailieu')
                link = group.get('link')

                list_material.append(
                    {
                        "Ten tai lieu" : tentailieu,
                        "Mo ta" : description,
                        "Loai tai lieu" : loaitailieu,
                        "Link" : link,
                    }   
                )

            return Response(
                {
                    'code' : 1000,
                    'message' : "OK",
                    'Thong tin lop hoc' : 
                    {
                        "Id lop hoc" : idlophoc,
                        "Ten lop hoc" : tenlophoc
                    },
                    'Danh sach tai lieu': list_material
                }, 
                status= status.HTTP_200_OK
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong!'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Edit material
    def put(self, request):
        try: 
            user= request.user
            if (not user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data=request.data
            idtailieu = data['idtailieu']
            if is_valid_param(idtailieu) == False:
                return Response(
                    {
                        'code' : 1004,
                        'message': 'Missing id info. Please add input' 
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if TaiLieuHocTap.objects.filter(idtailieu = idtailieu).count() == 0:
                return Response(
                    {
                        'code' : 9992,
                        'message': 'Material not found. Please try again.'
                    }
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            
            tentailieu = data['tentailieu']
            mota = data['mota']
            loaitailieu = data['loaitailieu']
            link = data['link']

            tailieu = TaiLieuHocTap.objects.get(idtailieu = idtailieu)

            if is_valid_param(tentailieu) == True:
                return Response(
                    {
                        'code' : 1006,
                        'message': 'Missing title info. Please add missing input' 
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if tailieu.tentailieu == tentailieu and tailieu.description == mota and tailieu.loaitailieu == loaitailieu and tailieu.link == link:
                return Response(
                    {
                        'code' : 1012,
                        'message': 'No info of file has not been modified' 
                    }, 
                    status=status.HTTP_304_NOT_MODIFIED
                )
            
            if len(mota) > 200:
                return Response(
                    {
                        'code' : 1013,
                        'message': 'The description was too long for the input field.' 
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            tailieu.tentailieu = tentailieu

            if is_valid_param(mota) == True:
                tailieu.description = mota
            
            if is_valid_param(loaitailieu) == True:
                tailieu.loaitailieu = loaitailieu

            if is_valid_param(link) == True:
                tailieu.link = link

            tailieu.save()

            tailieu_seria = TaiLieuHocTapSerializer(tailieu)

            return Response(
                {
                    'code' : 1000,
                    'message': "Update success",
                    'Thong tin tài liệu sau khi sửa ' : tailieu_seria.data,
                },
                status= status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Delete material
    def delete(self, request):
        try: 
            user= request.user
            if (not user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data=request.data
            idtailieu = data['idtailieu']
            if is_valid_param(idtailieu) == False:
                return Response(
                    {
                        'code' : 1004,
                        'message': 'Missing id info. Please add input' 
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if TaiLieuHocTap.objects.filter(idtailieu = idtailieu).count() == 0:
                return Response(
                    {
                        'code' : 9992,
                        'message': 'Material not found. Please try again.'
                    }
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            else: 
                tailieu = TaiLieuHocTap.objects.get(idtailieu = idtailieu)
                tailieu.delete()

            return Response(
                {
                    'code' : 1000,
                    'message': 'OK' 
                }
                ,status= status.HTTP_202_ACCEPTED
            )        

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetMaterialInfo(APIView):

    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        try:
            data=request.data
            idtailieu = data['idtailieu']
            if is_valid_param(idtailieu) == False:
                return Response(
                    {
                        'code' : 1004,
                        'message': 'Missing id info. Please add input' 
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if TaiLieuHocTap.objects.filter(idtailieu = idtailieu).count() == 0:
                return Response(
                    {
                        'code' : 9992,
                        'message': 'Material not found. Please try again.'
                    }
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            
            tailieu = TaiLieuHocTap.objects.get(idtailieu = idtailieu)
            tailieu_seria = TaiLieuHocTapSerializer(tailieu)

            return Response(
                {
                    'code' : 1000,
                    'message': 'OK',
                    'Thong tin chi tiet' :  tailieu_seria.data,
                }
                ,status= status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )