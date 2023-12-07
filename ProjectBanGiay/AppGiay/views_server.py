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

User = get_user_model()

# Create your views here.
def home(request) :
    try:
        khachhangaccount = TaikhoanKhachhang.objects.all()
        khach = TaiKhoanKGSerializer(khachhangaccount, many = True)
        return JsonResponse(data=khach.data, safe= False, status=status.HTTP_200_OK)
    except:
        traceback.print_exc()
        return Response(
            {'error': 'Something went wrong'},
                status= status.HTTP_400_BAD_REQUEST
        )



def id_generator (size = 5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


#Class quan li he thong nhan vien
class ManageAccount(APIView):
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
                                {"success": "Manager successfully created"},
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

    def put(self, request):
        try: 
            user= request.user
            if not user.is_manager:
                return Response({'error': 'User does not have necessary permission' }, status=status.HTTP_403_FORBIDDEN)
            else:
                number = request.data['id']
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

    def delete(self, request):
        try: 
            user= request.user
            if not user.is_manager:
                return Response({'error': 'User does not have necessary permission' }, status=status.HTTP_403_FORBIDDEN)
            else:
                number = request.data['id']
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
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['data'] = UserAccountSerializer(self.user).data
        return data


#Class quan li danh muc giay
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
        return JsonResponse({'List danh muc giay' :serializer.data}, safe= False)
    
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

    def delete(self, request):
        try:
            data=request.data
            serializer = self.serializer_class(data)
            if serializer.is_valid():
                giay = Danhmucgiay.objects.get(iddanhmuc=data['iddanhmuc'])
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
            tendanhmuc = data['tendanhmuc']
            loaigiay = data['loaigiay']
            hangsanxuat = data['hangsanxuat']
            giatien = data['giatien']
            doituong = data['doituong']
            danhmuc = Danhmucgiay.objects.filter(iddanhmuc = iddanhmuc).update(iddanhmuc = iddanhmuc, tendanhmuc = tendanhmuc, 
                                                                               loaigiay = loaigiay, hangsanxuat = hangsanxuat, 
                                                                               giatien = giatien, doituong = doituong)
            danhmuc_seria = self.serializer_class(danhmuc)
            return Response(
                {'Update success' : danhmuc_seria.data}, 
                status= status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#Class kiem soat order cua khachhang
def changestatus_1(request_data, iddonhang):
    confirmby = request_data['iddonhang']
    dvvanchuyen = request_data['iddonhang']
    tennv_vanchuyen = request_data['iddonhang']
    sdt = request_data['iddonhang']
    socccd = request_data['iddonhang']
    thoigiannhan = datetime.date.today()

    donhang = Donhang.objects.get(iddonhang = iddonhang) 
    donhang.trangthai = 'Đang giao' 
    donhang.confirmby = confirmby 
    donhang.dvvanchuyen = dvvanchuyen,
    donhang.tennv_vanchuyen = tennv_vanchuyen
    donhang.sdt = sdt
    donhang.socccd = socccd, 
    donhang.thoigiannhan = thoigiannhan
    donhang.save()

def changestatus_2(request_data, iddonhang):
    donhang = Donhang.objects.get(iddonhang = iddonhang)
    donhang.trangthai = 'Hoàn thành'
    donhang.save()

class ManageOrder(APIView):
    serializer_class = DonHangSerializer
    
    #Tra ve chi tiet thong tin don hang
    def get(self, request):
        donhang = Donhang.objects.order_by('iddonhang').all()
        serializer = DonHangSerializer(donhang, many=True)
        return JsonResponse({'List don hang cua khach' :serializer.data}, safe= False)

    def put(self, request, action):
        try:
            data = request.data
            if action == 1:
                changestatus_1(data)
            elif action == 2 :
                changestatus_2(data)
            else :
                return  Response(
                    {'error': 'Something went wrong'}, 
                    status= status.HTTP_400_BAD_REQUEST
                )
            return Response(
                    {'Update success'}, 
                    status= status.HTTP_202_ACCEPTED
                ) 
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
        

#Class quan li tai khoan khach hang
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

    def get(self, request):
        try:
            khachhangaccount = TaikhoanKhachhang.objects.all()
            taikhoan = TaiKhoanKGSerializer(khachhangaccount, many = True)
            return JsonResponse(data=taikhoan.data, safe= False, status=status.HTTP_200_OK)
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