from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Chitietdonhang,ChitiethoadonNhapHang,HoadonNhapHang,Donhang
from .models import Danhmucgiay,Chitietgiay,Khachhang,TaikhoanKhachhang,Reviewsanpham
from .models import UserAccount, UserAccountManager, U
from .serializers import ChitietDHSerializer,ChitietHDNHSerializer,HDNhapHangSerializer,DonHangSerializer
from .serializers import DanhMucGiaySerializer,ChitietGiaySerializer,KhachhangSerializer,TaiKhoanKGSerializer,ReviewSPSerializer
from .serializers import UserAccountSerializer
from django.contrib.auth import get_user_model
import traceback
import random, string
import datetime

User = get_user_model()

# Create your views here.
def home(request) :
    return HttpResponse("Hello there")

def id_generator (size = 5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#Class quan li he thong
class CreateAccount(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request):
        try:
            data = request.data
            
            email = data['email']
            email = email.lower()
            password = data['password']
            tennhanvien = data['fullName']
            tenchucvu = data['role']
            gioitinh = data['gioitinh']
            ngaysinh = data['ngaysinh']
            date_joined = datetime.date.today()

            re_password = data['re_password']
            
            # TODO: the logic in the signup
            is_mangaer = data['is_manager']
            
            if password ==  re_password:
                if len(password) >= 8:
                    if not User.objects.filter(email=email).exists():
                        if not is_mangaer:
                            UserAccountManager.create_user(email = email, tennhanvien = tennhanvien, tenchucvu = tenchucvu, gioitinh = gioitinh, ngaysinh = ngaysinh, date_joined = date_joined, password=password)
                            return Response(
                                {"success": "User successfully created"},
                                status= status.HTTP_201_CREATED
                            )
                        else: 
                            UserAccountManager.create_manager(email = email, tennhanvien = tennhanvien, tenchucvu = tenchucvu, gioitinh = gioitinh, ngaysinh = ngaysinh, date_joined = date_joined, password=password)
                            return Response(
                                {"success": "Teacher successfully created"},
                                status= status.HTTP_201_CREATED
                            )
                    else:
                        return Response(
                        {'error': 'Email already exist'},
                        status= status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                    {'error': 'Password must have more than 8 character'},
                    status= status.HTTP_400_BAD_REQUEST
                    )
                    
            else:
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

class RetrieveAccountView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserAccountSerializer(user)
            
            return Response(
                {
                    'user': user.data,
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateAccountView(APIView):
    def put(self, request, number):
        try: 
            user= request.user
            if not user.is_manager:
                return Response({'error': 'User does not have necessary permission' }, status=status.HTTP_403_FORBIDDEN)
            else:
                account = UserAccount.objects.get(id=number)
                serializer = UserAccountSerializer(account, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(
                        {'error': 'Mismatch data. Please check again'}, 
                        status= status.HTTP_400_BAD_REQUEST
                    )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteAccount(APIView):
    def delete(self, request, number):
        try: 
            user= request.user
            if not user.is_manager:
                return Response({'error': 'User does not have necessary permission' }, status=status.HTTP_403_FORBIDDEN)
            else:
                account = UserAccount.objects.get(id=number)
                account.delete()
                return Response(
                    {'error': 'Delete successful'}, 
                    status= status.HTTP_204_NO_CONTENT
                )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

#Class quan li ban giay
def insert_danhmucgiay(requested_data):
    tendanhmuc = requested_data['tendanhmuc']
    loaigiay = requested_data['loaigiay']
    hangsanxuat = requested_data['hangsanxuat']
    giatien = requested_data['giatien']
    doituong = requested_data['doituong']
    
    danhmucgiay = Danhmucgiay(tendanhmuc = tendanhmuc, loaigiay = loaigiay, hangsanxuat = hangsanxuat, giatien = giatien, doituong = doituong)
    danhmucgiay.save()
    
    return danhmucgiay

class DanhMucGiayManage(APIView):
    serializer_class = DanhMucGiaySerializer
    serializer_class1 = ChitietGiaySerializer

    def get_list(self, request):
        giay = Danhmucgiay.objects.order_by('iddanhmuc').all()
        serializer = self.serializer_class(giay, many=True)
        return Response(serializer.data, safe= False)

    def get_detail(self, request, number):
        try :
            view = Danhmucgiay.objects.get(pk=number)
        except view.DoesNotExits :
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        tonggiay = Chitietgiay.objects.filterby(iddanhmuc = view.iddanhmuc)
        serializer = self.serializer_class1(tonggiay, many= True)
        return Response(serializer.data, safe=False)
    
    def post(self, request):
        try: 
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                insert_danhmucgiay(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
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

    def delete(self, request, number):
        try: 
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                giay = Danhmucgiay.objects.get(iddanhmuc=number)
                giay.delete()
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

class ChiTietGiayManager(APIView):
    pass


