from django.shortcuts import render , HttpResponse
from django.http import JsonResponse
from pymysql import NULL
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Chitietdonhang,ChitiethoadonNhapHang,HoadonNhapHang,Donhang
from .models import Danhmucgiay,Chitietgiay,Khachhang,TaikhoanKhachhang,Reviewsanpham
from .models import UserAccount, UserAccountManager
from .serializers import ChitietDHSerializer,ChitietHDNHSerializer,HDNhapHangSerializer,DonHangSerializer
from .serializers import DanhMucGiaySerializer,ChitietGiaySerializer,KhachhangSerializer,TaiKhoanKGSerializer,ReviewSPSerializer
from .serializers import UserAccountSerializer
from django.contrib.auth import get_user_model
import traceback
import random, string
import datetime


class KhachHangAccountManager(APIView):

    serializer_class = TaiKhoanKGSerializer

    def post(self, request):
        try:
            data = request.data
            
            while True:
                taikhoan = id_generator(size=10)
                if (TaikhoanKhachhang.objects.filter(idtaikhoan = taikhoan).count() == 0):
                    break
            
            idkhachhang = data['idkhachhang']
            username = data['username']
            password = data['password']
            gioitinh = data['gioitinh']
            ngaysinh = data['ngaysinh']
            ngaylapTK = datetime.date.today()

            re_password = data['re_password']

            if password ==  re_password:
                if len(password) >= 8:
                    if not TaikhoanKhachhang.objects.filter(idkhachhang = idkhachhang).exists():
                        if not TaikhoanKhachhang.objects.filter(username = username).exists():
                            taikhoanMoi = TaikhoanKhachhang(idtaikhoan = taikhoan, idkhachhang = idkhachhang, username = username,
                                                        gioitinh = gioitinh, ngaysinh= ngaysinh, ngaylapTK = ngaylapTK)
                            taikhoanMoi.save()
                            taikhoanMoi = TaiKhoanKGSerializer(taikhoanMoi)
                            return Response(
                                {"Account successfully created" : taikhoanMoi.data},
                                status= status.HTTP_201_CREATED
                            )
                        else:
                            traceback.print_exc()
                            return Response(
                                {'error': 'Username already exist'},
                                status= status.HTTP_400_BAD_REQUEST
                            )
                    else:
                        traceback.print_exc()
                        return Response(
                        {'error': 'Account already exist'},
                        status= status.HTTP_400_BAD_REQUEST
                        )
                else:
                    traceback.print_exc()
                    return Response(
                    {'error': 'Password must have more than 8 character'},
                    status= status.HTTP_400_BAD_REQUEST
                    )
                    
            else:
                traceback.print_exc()
                return Response(
                    {'error': 'Password do not match'},
                    status= status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong!'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request, format=None):
        permission_classes = (permissions.AllowAny, )

        try:
            khachhangaccount = TaikhoanKhachhang.objects.all()
            taikhoan = TaiKhoanKGSerializer(khachhangaccount, many = True)
            return Response(data=taikhoan.data, safe= False, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        try: 
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                idtaikhoan = request.data['idtaikhoan']
                list_review = Reviewsanpham.objects.filter(idtaikhoan = idtaikhoan)
                for group in list_review.data:
                    review = Reviewsanpham.objects.get(idtaikhoan = group.get('idtaikhoan'))
                    review.delete()
                taikhoan = TaikhoanKhachhang.objects.get(idtaikhoan = idtaikhoan)
                taikhoan.delete()
                return Response(
                    {'error': 'Delete successful'}, 
                    status= status.HTTP_204_NO_CONTENT
                )
            else:
                return  Response(
                    {'error': 'Something went wrong'}, 
                    status= status.HTTP_400_BAD_REQUEST
                )            
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )