from django.shortcuts import HttpResponse
from django.http import JsonResponse
from pymysql import NULL
from rest_framework import generics, permissions, status, authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import Chitietdonhang,ChitiethoadonNhapHang,HoadonNhapHang,Donhang
from .models import Danhmucgiay,Chitietgiay,Khachhang,Reviewsanpham,Nhanvien
from .models import UserAccount, UserAccountManager
from .serializers import ChitietDHSerializer,ChitietHDNHSerializer,HDNhapHangSerializer,DonHangSerializer
from .serializers import DanhMucGiaySerializer,ChitietGiaySerializer,KhachhangSerializer,ReviewSPSerializer
from .serializers import UserAccountSerializer
from django.contrib.auth import get_user_model
import traceback
import random, string
import datetime

User = get_user_model()

# Create your views here.
def is_valid_param(param) :
    return param != " " and param is not None


def id_generator (size = 5, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def insert_khachhang(requested_data,Email,accountName,user):
    while True:
        khachhang = id_generator(size=5)
        if (Khachhang.objects.filter(idkhachhang=khachhang).count() == 0):
            break
    tenkhachhang = accountName
    email = Email
    diachi = requested_data['diachi']
    sdt = requested_data['sdt']
    user_id = user
    diemtichluy = 0
    
    customer = Khachhang(idkhachhang=khachhang,tenkhachhang=tenkhachhang, 
                         email=email,diachi=diachi,sdt=sdt,diemtichluy=diemtichluy, id = user_id)
    customer.save()
    
    return customer

def insert_nhanvien(requested_data,Email,accountName,user):
    while True:
        nhanvien = id_generator(size=5)
        if (Nhanvien.objects.filter(idnhanvien=nhanvien).count() == 0):
            break
    tennhanvien = accountName
    email = Email
    tenchucvu = requested_data['tenchucvu']
    diachi = requested_data['diachi']
    sdt = requested_data['sdt']
    user_id = user
    
    manager = Nhanvien(idnhanvien=nhanvien,tennhanvien=tennhanvien, tenchucvu=tenchucvu
                        ,diachi=diachi,sdt=sdt, id = user_id)
    manager.save()
    
    return manager

#Class quan li he thong nhan vien
class ManageAccount(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request):
        try:
            data = request.data
            
            password = data['password']
            email = data['email']
            email = email.lower()
            accountname = data['accountname']
            gioitinh = data['gioitinh']
            ngaysinh = data['ngaysinh']
            date_joined = datetime.date.today()

            re_password = data['re_password']
            
            # TODO: the logic in the signup
            is_manager = data['is_manager']
            
            if password ==  re_password:
                if len(password) >= 8:
                    if not UserAccount.objects.filter(email=email).exists():
                        if not is_manager:
                            customer = User.objects.create_customer(email = email, accountname=accountname, sex = gioitinh, 
                                                                  brithday = ngaysinh, joined = date_joined, password=password)
                            insert_khachhang(requested_data=data,Email=email,accountName=accountname,user=customer)
                            return Response(
                                {"success": "User successfully created"},
                                status= status.HTTP_201_CREATED
                            )
                        else: 
                            manager = User.objects.create_manager(email = email, accountname=accountname, sex = gioitinh, 
                                                                  brithday = ngaysinh, joined = date_joined, password=password)
                            insert_nhanvien(requested_data=data,Email=email,accountName=accountname,user=manager)
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
            userAll = UserAccount.objects.all()
            user = UserAccountSerializer(userAll, many=True)
            return Response(
                {'user': user.data,},
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
                gioitinh = request.data['gioitinh']
                ngaysinh = request.data['ngaysinh']
                account = UserAccount.objects.get(id=number)
                account.gioitinh = gioitinh
                account.ngaysinh = ngaysinh
                account.save()
                user_seria = UserAccountSerializer(account)
                return Response(
                    {'Update success': user_seria.data}, 
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
            user= request.user
            if not user.is_manager:
                return Response({'error': 'User does not have necessary permission' }, status=status.HTTP_403_FORBIDDEN)
            else:
                number = request.data['id']
                account = UserAccount.objects.get(id=number)
                account.delete()
                return Response(
                    {'error': 'Delete successful'}, 
                    status= status.HTTP_200_OK
                )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RetriveUserView(APIView):

    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        try:
            user = request.user
            user_seria = UserAccountSerializer(user)
            return Response(
                {'user': user_seria.data,},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#Class quan li danh muc giay
class ManageDanhMucGiay(APIView):
    serializer_class = DanhMucGiaySerializer
    serializer_class1 = ChitietGiaySerializer

    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        try:
            data = request.data
            loaigiay = data['loaigiay']
            hangsanxuat = data['hangsanxuat']
            tugiatien = data['tugiatien']
            dengiatien = data['dengiatien']
            doituong = data['doituong']

            danhmucgiay = Danhmucgiay.objects.all()

            if is_valid_param(loaigiay):
                danhmucgiay = danhmucgiay.filter(loaigiay=loaigiay)

            if is_valid_param(tugiatien):
                danhmucgiay = danhmucgiay.filter(giatien__gte = tugiatien)

            if is_valid_param(dengiatien):
                danhmucgiay = danhmucgiay.filter(giatien__lte = dengiatien)

            if is_valid_param(hangsanxuat):
                danhmucgiay = danhmucgiay.filter(hangsanxuat = hangsanxuat)

            if is_valid_param(doituong):
                danhmucgiay = danhmucgiay.filter(doituong = doituong)
            
            serializer = self.serializer_class(danhmucgiay, many=True)
            return JsonResponse({'List danh muc giay' : serializer.data}, safe= False)
        except:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_400_BAD_REQUEST
            )
    
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
                list_chitiet = Chitietgiay.objects.filter(iddanhmuc=iddanhmuc)
                for group in list_chitiet:
                    group.delete()
                danhmucgiay = Danhmucgiay.objects.get(iddanhmuc=iddanhmuc)
                danhmucgiay.delete()
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


class ManageChitietGiay(APIView):

    permission_classes = (permissions.AllowAny, )

    def post(self,request):
        try:
            serializer = ChitietGiaySerializer(data=request.data)
            if serializer.is_valid():
                while True:
                    idgiay = id_generator(size=6)
                    if (Chitietgiay.objects.filter(idgiay=idgiay).count() == 0):
                        break
                iddanhmuc = serializer.data.get('iddanhmuc')
                kichco = serializer.data.get('kichco')
                mausac = serializer.data.get('mausac')
                sotonkho = serializer.data.get('sotonkho')
    
                maugiay = Chitietgiay(idgiay=idgiay, iddanhmuc = Danhmucgiay(iddanhmuc=iddanhmuc), 
                                      kichco=kichco, mausac= mausac, sotonkho=sotonkho)
                maugiay.save()
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

    def get(self, request):
        list_chitiet = []

        try:
            data = request.data
            iddanhmuc = data['iddanhmuc']
            danhmuc = Danhmucgiay.objects.get(iddanhmuc=iddanhmuc)
            serializer = DanhMucGiaySerializer(danhmuc)
            tendanhmuc = serializer.data.get('tendanhmuc')
            giatien = serializer.data.get('giatien')
            list_giay = Chitietgiay.objects.filter(iddanhmuc = iddanhmuc)
            list_giay_seria = ChitietGiaySerializer(list_giay, many = True)
            for group in list_giay_seria.data:
                giay = Chitietgiay.objects.get(idgiay = group.get('idgiay'))
                #Neu het hang , bo qua mau giay nay
                idgiay = giay.idgiay
                colour = giay.mausac
                size = giay.kichco
                soluong = giay.sotonkho
                list_chitiet.append(
                    {
                        'id mau giay' : idgiay,
                        'kich thuoc' : size,
                        'mausac' : colour,
                        'So ton kho' : soluong,
                    }
            )
            return JsonResponse(
                {
                    'Thong tin thong ke' : 
                    {
                        'Ten danh muc' : tendanhmuc,
                        'Gia tien' : giatien,
                        'Cac mau giay' : list_chitiet
                    }
                }
                , safe= False
                , status=status.HTTP_200_OK
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
            idgiay = data['idgiay']
            sotonkho = data['sotonkho']
            maugiay = Chitietgiay.objects.filter(idgiay=idgiay)
            if maugiay.count() == 0:
                return JsonResponse(
                    {'error': 'No matching'}
                    , safe=False 
                    ,status= status.HTTP_403_FORBIDDEN
                )
            else:
                maugiay.update(idgiay=idgiay, sotonkho=sotonkho)
                maugiay_seria = ChitietGiaySerializer(maugiay, many= True)
                return JsonResponse(
                    {'Update success' : maugiay_seria.data}
                    , safe=False 
                    ,status= status.HTTP_202_ACCEPTED
                )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self,request):
        try:
            data=request.data
            idgiay=data['idgiay']
            if Chitietgiay.objects.filter(idgiay=idgiay).count() == 0:
                return JsonResponse(
                    {'error': 'No matching'}
                    ,safe=False 
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            else:
                giay = Chitietgiay.objects.get(idgiay=idgiay)
                giay.delete()
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


#Class kiem soat order cua khachhang
class ManageOrder(APIView):
    serializer_class = DonHangSerializer

    permission_classes = (permissions.AllowAny, )
    
    #Tra ve chi tiet thong tin don hang
    def get(self, request):
        try:
            data = request.data
            tungay = data['tu ngay']
            denngay = data['den ngay']
            trangthai = data['trangthai']
            if denngay < tungay:
                 return Response(
                    {'error': 'From day must not set behind to date'},
                    status= status.HTTP_400_BAD_REQUEST
                )
            donhang = Donhang.objects.order_by('iddonhang').all()

            if is_valid_param(tungay):
                donhang = donhang.filter(createday__gte = tungay)

            if is_valid_param(denngay):
                donhang = donhang.filter(createday__lte = denngay)

            if is_valid_param(trangthai):
                donhang = donhang.filter(trangthai=trangthai)

            serializer = self.serializer_class(donhang, many=True)
            return JsonResponse(
                {
                    'List don hang cua khach' :serializer.data
                }
                ,safe= False)
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
            if action == 0:
                confirmby = data['iddonhang']
                dvvanchuyen = data['iddonhang']
                tennv_vanchuyen = data['iddonhang']
                sdt = data['iddonhang']
                socccd = data['iddonhang']
                thoigiannhan = datetime.datetime.now()

                donhang = Donhang.objects.get(iddonhang = iddonhang) 
                donhang.trangthai = 'Đang giao' 
                donhang.confirmby = confirmby 
                donhang.dvvanchuyen = dvvanchuyen,
                donhang.tennv_vanchuyen = tennv_vanchuyen
                donhang.sdt = sdt
                donhang.socccd = socccd, 
                donhang.thoigiannhan = thoigiannhan
                donhang.save()
            elif action == 1 :
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
                list_giay = Chitietdonhang.objects.filter(iddonhang = iddonhang)
                if list_giay.count() != 0:
                    list_giay_seria = ChitietDHSerializer(list_giay, many = True)
                    for group in list_giay_seria.data:
                        giay = Chitietdonhang.objects.get(idchitiet = group.get('idchitiet'))
                        giay.delete()
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
