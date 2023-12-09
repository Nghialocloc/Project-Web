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



def id_generator (size = 5, chars=string.digits):
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
class ManageDanhMucGiay(APIView):
    serializer_class = DanhMucGiaySerializer
    serializer_class1 = ChitietGiaySerializer

    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        giay = Danhmucgiay.objects.order_by('iddanhmuc').all()
        serializer = self.serializer_class(giay, many=True)
        return JsonResponse({'List danh muc giay' :serializer.data}, safe= False)
    
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                while True:
                    danhmuc = id_generator(size=5)
                    if (Danhmucgiay.objects.filter(iddanhmuc = danhmuc).count() == 0):
                        break
                tendanhmuc = serializer.data.get('tendanhmuc')
                loaigiay = serializer.data.get('loaigiay')
                hangsanxuat = serializer.data.get('hangsanxuat')
                giatien = serializer.data.get('giatien')
                doituong = serializer.data.get('doituong')
    
                danhmucgiay = Danhmucgiay(iddanhmuc = danhmuc, tendanhmuc = tendanhmuc, loaigiay = loaigiay, hangsanxuat = hangsanxuat, giatien = giatien, doituong = doituong)
                danhmucgiay.save()
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
            else:
                traceback.print_exc()
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
            iddanhmuc=data['iddanhmuc']
            if Danhmucgiay.objects.filter(iddanhmuc=iddanhmuc).count() == 0:
                return JsonResponse(
                    {'error': 'No matching'}
                    ,safe=False 
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            else:
                giay = Danhmucgiay.objects.get(iddanhmuc=iddanhmuc)
                giay.delete()
                return JsonResponse(
                    {'error': 'Delete successful'}
                    ,safe=False 
                    ,status= status.HTTP_204_NO_CONTENT
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
            danhmuc = Danhmucgiay.objects.filter(iddanhmuc = iddanhmuc)
            if danhmuc.count() == 0:
                return JsonResponse(
                    {'error': 'No matching'}
                    , safe=False 
                    ,status= status.HTTP_403_FORBIDDEN
                )
            else:
                danhmuc.update(iddanhmuc = iddanhmuc, tendanhmuc = tendanhmuc, 
                        loaigiay = loaigiay, hangsanxuat = hangsanxuat, 
                        giatien = giatien, doituong = doituong)
                danhmuc_seria = self.serializer_class(danhmuc, many= True)
                return JsonResponse(
                    {'Update success' : danhmuc_seria.data}
                    , safe=False 
                    ,status= status.HTTP_202_ACCEPTED
                )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#Class kiem soat order cua khachhang
class ManageOrder(APIView):
    serializer_class = DonHangSerializer

    permission_classes = (permissions.AllowAny, )
    
    #Tra ve chi tiet thong tin don hang
    def get(self, request):
        try:
            donhang = Donhang.objects.order_by('iddonhang').all()
            serializer = self.serializer_class(donhang, many=True)
            return JsonResponse({'List don hang cua khach' :serializer.data}, safe= False)
        except:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_400_BAD_REQUEST
            )

    def put(self, request):
        try:
            data = request.data
            iddonhang = data['iddonhang']
            action = data['action']
            if action == 1:
                confirmby = data['iddonhang']
                dvvanchuyen = data['iddonhang']
                tennv_vanchuyen = data['iddonhang']
                sdt = data['iddonhang']
                socccd = data['iddonhang']
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
            elif action == 2 :
                donhang = Donhang.objects.get(iddonhang = iddonhang)
                donhang.trangthai = 'Hoàn thành'
                donhang.save()
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
            data=request.data
            iddonhang = data['iddonhang']
            if Donhang.objects.filter(iddonhang = iddonhang).count() == 0:
                return JsonResponse(
                    {'error': 'No matching'}
                    ,safe=False 
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            else:
                donhang = Donhang.objects.get(iddonhang = iddonhang)
                donhang.delete()
                return JsonResponse(
                    {'error': 'Delete successful'}
                    ,safe=False 
                    ,status= status.HTTP_204_NO_CONTENT
                )        
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

#Class quan li tai khoan khach hang
class ManageKhachHangAccount(APIView):

    serializer_class = TaiKhoanKGSerializer

    permission_classes = (permissions.AllowAny, )

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
        
