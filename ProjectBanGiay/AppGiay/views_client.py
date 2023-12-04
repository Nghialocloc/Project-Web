from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from pymysql import NULL
from rest_framework import generics, permissions, status, viewsets
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
from django_filters import rest_framework as filter
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
        soluong = request_data['soluong']
        dongia = request_data['dongia']
        if (Donhang.objects.filter(iddonhang = iddonhang).count() == 0):
            return Response(
                {'error': 'Order not exist'}, 
                status= status.HTTP_404_NOT_FOUND
            )            
        CTdonhang = Chitietdonhang(iddonhang=iddonhang, idgiay=idgiay, soluong=soluong, dongia=dongia)
        CTdonhang.save()
        return Response(
            {'Cap nhat': ChitietDHSerializer(CTdonhang).data}, 
            status= status.HTTP_200_OK
        )                     
            

def remove_giay(request_data):
    CTdonhang = Chitietdonhang.objects.get(iddonhang= request_data['iddonhang'],
                                            idgiay= request_data['idgiay'], 
                                            soluong= request_data['soluong'])
    CTdonhang.delete()
    return Response(
        {'error': 'Delete successful'}, 
        status= status.HTTP_204_NO_CONTENT
    )

#Class kiem soat gio hang
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

    def put(self, request, condition):
        try:
            data = request.data
            serializer = self.serializer_class(data)
            if serializer.is_valid():
                if condition == 0:
                    add_giay(serializer.data)
                elif condition == 1:
                    remove_giay(serializer.data)
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


#Class tim kiem cho client va server
class GiayFilter(filter.FilterSet):
    hangsanxuat = filter.ModelMultipleChoiceFilter(field_name= 'Mau sac', query = Danhmucgiay.hangsanxuat.__get__)
    loaigiay = filter.ModelMultipleChoiceFilter(field_name= 'Kich thuoc', query = Danhmucgiay.loaigiay.__get__)
    doituong = filter.ModelMultipleChoiceFilter(field_name= 'Doi tuong', query = Danhmucgiay.doituong.__get__)


class GiayViewSet(viewsets.ModelViewSet):
    queryset = Danhmucgiay.objects.all()
    serializer_class = DanhMucGiaySerializer
    filter_class = GiayFilter


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

#Class kiem soat review khach hang
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