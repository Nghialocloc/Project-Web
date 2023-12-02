from django.shortcuts import render, HttpResponse
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

User = get_user_model()

# Create your views here.
def home(request) :
    return HttpResponse("Hello there")

def id_generator (size = 5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#Class quan li he thong nhan vien
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
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['data'] = UserAccountSerializer(self.user).data
        return data

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
        

#Class quan li danh muc giay cho server
def insert_danhmucgiay(requested_data, iddanhmuc):
    tendanhmuc = requested_data['tendanhmuc']
    loaigiay = requested_data['loaigiay']
    hangsanxuat = requested_data['hangsanxuat']
    giatien = requested_data['giatien']
    doituong = requested_data['doituong']
    
    danhmucgiay = Danhmucgiay(iddanhmuc = iddanhmuc, tendanhmuc = tendanhmuc, loaigiay = loaigiay, hangsanxuat = hangsanxuat, giatien = giatien, doituong = doituong)
    danhmucgiay.save()
    
    return danhmucgiay

class DanhMucGiayManage(APIView):
    serializer_class = DanhMucGiaySerializer
    serializer_class1 = ChitietGiaySerializer

    def get(self, request):
        giay = Danhmucgiay.objects.order_by('iddanhmuc').all()
        serializer = self.serializer_class(giay, many=True)
        return Response({'List danh muc giay' :serializer.data}, safe= False)
    
    def post(self, request):
        try: 
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                while True:
                    danhmuc = id_generator(size=10)
                    if (Danhmucgiay.objects.filter(iddanhmuc = danhmuc).count() == 0):
                        break
                insert_danhmucgiay(serializer.data, danhmuc)
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

    def put(self, request):
        try: 
            data= request.data
            iddanhmuc = data['iddanhmuc']
            serializer = self.serializer_class(data=request.data)
            insert_danhmucgiay(serializer.data, iddanhmuc)
            return Response(
                {'error': 'Update success'}, 
                status= status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

#Class tim kiem cho client
class TimKiemGiayManager(APIView):
    def get(self, request):
        pass

    def timkiem_mausac(request):
        pass

    def timkiem_kichco(request):
        pass

    def timkiem_hangsanxuat(request):
        pass

    def timkiem_giatien(request):
        pass

    def timkiem_loaigiay(request):
        pass

    def timkiem_doituong(request):
        pass

#Class kiem soat cho client
class ManageGioHang(APIView):

    serializer_class = DonHangSerializer

    # Tao lan dau tien
    def post(self, request):
        try: 
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                while True:
                    iddonhang = id_generator(size=10)
                    if (Donhang.objects.filter(iddonhang = iddonhang).count() == 0):
                        break
                idkhachhang = serializer.data.get('idkhachhang')
                idkhachhang = Khachhang.objects.get(idkhachhang=idkhachhang)
                createday = datetime.date.today()
                trangthai = 'Checking'
                donhangtm = Donhang(iddonhang = iddonhang, idkhachhang = idkhachhang, createday = createday, trangthai = trangthai,
                                    confirmby = NULL, dvvanchuyen = NULL,tennv_vanchuyen = NULL,sdt = NULL, socccd = NULL, thoigiannhan = NULL)
                donhangtm.save()
                return Response(DonHangSerializer(donhangtm).data, status=status.HTTP_201_CREATED)
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
    
    #Tra ve list cac danh muc trong gio
    def get(self, request):
        try:
            data = request.data
            iddonhang = data['iddonhang']
            donhang = Donhang.objects.get(iddonhang=iddonhang)
            donhang = self.serializer_class(data= donhang)
            if donhang.is_valid():
                return Response({'Don hang khach tam thoi': donhang.data}, status=status.HTTP_200_OK)
            else :
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

    def put(self, request):
        pass

    def delete(self, request):
        try: 
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                iddonhang = request.data['iddonhang']
                donhang = Donhang.objects.get(iddonhang = iddonhang)
                donhang.delete()
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

    #Chinh sua chi tiet don hang
    def add_giay(request):
        pass

    def remove_giay(request):
        pass
    

#Class quan li khach hang cho server
class KhachHangAccountManager(APIView):
    def post(self, request):
        pass

    def put(self, request):
        pass

    def get(self, request):
        pass

    def delete(self, request):
        pass

class KhachHangAccountActivities(APIView):
    #Lay lich su mua hang cua khach
    def get(self, request):
        pass


class ReviewManager(APIView):
    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass


# class MuaBanManager(APIView):
#     def get(self, request, number):
#         chitietgiay_list = []
#         colour_list = []
#         size_list = []

#         try :
#             view = Danhmucgiay.objects.get(iddanhmuc = number)
#         except view.DoesNotExits :
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         chitietgiay = Chitietgiay.objects.filterby(iddanhmuc = view.iddanhmuc)
#         chitietgiay_list.append(ChitietGiaySerializer(chitietgiay).data)
#         return Response({ 'Thong tin chi tiet' : chitietgiay_list}, safe=False)
