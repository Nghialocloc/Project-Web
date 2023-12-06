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
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
import django_filters
import traceback
import random, string
import datetime

User = get_user_model()

def id_generator (size = 5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


#Chinh sua chi tiet don hang
def add_giay(request_data):
    iddonhang = request_data['iddonhang']
    idgiay = request_data['idgiay']
    giay = Danhmucgiay.objects.get(idgiay=idgiay)
    money = giay.giatien
    soluong = request_data['soluong']
    dongia = soluong * money
    if (Donhang.objects.filter(iddonhang = iddonhang).count() == 0):
        return Response(
            {'error': 'Order not exist'}, 
            status= status.HTTP_404_NOT_FOUND
        )            
    CTdonhang = Chitietdonhang(iddonhang=iddonhang, idgiay=idgiay, soluong=soluong, dongia=dongia)
    CTdonhang.save()
    
    return dongia
            

def remove_giay(request_data):
    CTdonhang = Chitietdonhang.objects.get(iddonhang= request_data['iddonhang'],
                                            idgiay= request_data['idgiay'], 
                                            soluong= request_data['soluong'])
    remove = CTdonhang.dongia
    CTdonhang.delete()
    return remove

def cofirm_donhang(request_data):
    iddonhang = request_data['iddonhang']
    if (Donhang.objects.filter(iddonhang = iddonhang).count() == 0):
        return Response(
            {'error': 'Order not exist'}, 
            status= status.HTTP_404_NOT_FOUND
        )
    else:
        donhang = Donhang.objects.get(iddonhang = iddonhang)
        donhang.trangthai = 'Confirm'
        donhang.save()
        return Response(DonHangSerializer(donhang).data, status=status.HTTP_202_ACCEPTED)


#Class kiem soat gio hang cho khach hang
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
            list_giay = []
            data = request.data
            iddonhang = data['iddonhang']
            donhang = Donhang.objects.get(iddonhang=iddonhang)
            donhang_seria = self.serializer_class(donhang)

            if donhang_seria.is_valid():
                danhsachgiay = Chitietdonhang.objects.filter(iddonhang = donhang.iddonhang)
                for group in danhsachgiay.data:
                    giay = Chitietgiay.objects.get(idgiay = group.get('idgiay'))
                    mausac = giay.mausac
                    kichthuoc = giay.kichco

                    danhmucgiay = Danhmucgiay.objects.get(iddanhmuc = giay.iddanhmuc)
                    danhmucgiay_seria = DanhMucGiaySerializer(danhmucgiay)
                        
                    CTdonhang = Chitietdonhang.objects.get(iddonhang=giay.iddanhmuc, idgiay = group.get('idgiay'))
                    soluong = CTdonhang.soluong

                    list_giay.append(
                        {
                            'Mau giay' : danhmucgiay_seria,
                            'Thong tin chi tiet' : {mausac,kichthuoc},
                            'So luong' : soluong
                        }
                    )
                return Response(
                    {
                        'Ma don hang' : iddonhang,
                        'Don hang khach hien tai': list_giay
                    }, 
                    status=status.HTTP_200_OK
                )
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

    def put(self, request, action):
        try:
            data = request.data
            serializer = self.serializer_class(data)
            iddonhang = data['iddonhang']
            donhang = Donhang.objects.get(iddonhang = iddonhang)
            if serializer.is_valid():
                if action == 0:
                    money = add_giay(serializer.data)
                    donhang.sotienthanhtoan += money
                    donhang.save()
                elif action == 1:
                    remove_giay(serializer.data)
                    donhang.sotienthanhtoan -= money
                    donhang.save()
                elif action == 2:
                    cofirm_donhang(serializer.data)
                return Response(
                    {'Update success'}, 
                    status= status.HTTP_202_ACCEPTED
                )
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

    def delete(self, request):
        try:
            data=request.data
            serializer = self.serializer_class(data)
            if serializer.is_valid():
                iddonhang = data['iddonhang']
                list = Chitietdonhang.objects.filter(iddonhang = iddonhang)
                list.delete()
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


#Cac class tim kiem cho client va server
class GiayFilter(django_filters.FilterSet):
    tendanhmuc = django_filters.CharFilter(field_name= 'tendanhmuc', label= 'Search',ookup_expr='iexact')


class GiayList(generics.ListAPIView):
    queryset = Danhmucgiay.objects.all()
    serializer_class = DanhMucGiaySerializer
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = GiayFilter


def get_listgiay(request):
    giay_filter = GiayFilter(request.GET, queryset = Danhmucgiay.objects.all())
    context = {
        'form' : giay_filter.form,
        'giay' : giay_filter.qs
    }
    return render(request, '', context)


#Class kiem soat review khach hang
class ReviewManager(APIView):
    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass


#Lay lich su mua hang cua khach cho server and client
class KhachHangAccountActivities(APIView):
    def get(self, request):
        pass