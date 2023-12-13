from django.shortcuts import HttpResponse
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

def is_valid_param(param) :
    return param != '' and param is not None

def id_generator (size = 5, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


#Chinh sua chi tiet don hang
def add_giay(request_data,iddanhmuc,soluong, mausac, kichco):
    while True:
        idchitiet = id_generator(size=5)
        if (Chitietdonhang.objects.filter(idchitiet = idchitiet).count() == 0):
            break
    iddonhang = request_data['iddonhang']
    danhmuc = Danhmucgiay.objects.get(iddanhmuc=iddanhmuc)
    money = danhmuc.giatien
    dongia = soluong * money

    giay = Chitietgiay.objects.get(iddanhmuc=iddanhmuc, mausac=mausac, kichco=kichco)
    idgiay = giay.idgiay
    if (Donhang.objects.filter(iddonhang = iddonhang).count() == 0):
        return Response(
            {'error': 'Order not exist'}, 
            status= status.HTTP_404_NOT_FOUND
        )            
    CTdonhang = Chitietdonhang(idchitiet= idchitiet, iddonhang=Donhang(iddonhang=iddonhang), idgiay=Chitietgiay(idgiay=idgiay), 
                               soluong=soluong, dongia=dongia)
    CTdonhang.save()
    
    return dongia
            

def remove_giay(request_data,idchitiet):
    iddonhang = request_data['iddonhang']
    if (Donhang.objects.filter(iddonhang = iddonhang).count() == 0):
        return Response(
            {'error': 'Order not exist'}, 
            status= status.HTTP_404_NOT_FOUND
        )            
    CTdonhang = Chitietdonhang.objects.get(idchitiet= idchitiet)
    money = CTdonhang.dongia
    CTdonhang.delete()
    return money

def cofirm_donhang(request_data, tenkhachhang,diachi,email,sdt):
    iddonhang = request_data['iddonhang']
    idkhachhang = request_data['idkhachhang']
    if (Donhang.objects.filter(iddonhang = iddonhang).count() == 0):
        return Response(
            {'error': 'Order not exist'}, 
            status= status.HTTP_404_NOT_FOUND
        )
    elif idkhachhang != 10000:
        donhang = Donhang.objects.get(iddonhang = iddonhang)
        donhang.trangthai = 'Confirm'
        donhang.save()
        return Response(DonHangSerializer(donhang).data, status=status.HTTP_202_ACCEPTED)
    else:
        while True:
            idkh = id_generator(size=5)
            if (Khachhang.objects.filter(idkhachhang = idkh).count() == 0):
                break
        khachhang = Khachhang(idkhachhang = idkh, tenkhachhang=tenkhachhang, diachi=diachi, email=email, sdt=sdt)
        khachhang.save()

        donhang = Donhang.objects.get(iddonhang = iddonhang)
        donhang.idkhachhang = Khachhang(idkhachhang=idkh)
        donhang.trangthai = 'Confirm'
        donhang.save()
        return Response(DonHangSerializer(donhang).data, status=status.HTTP_202_ACCEPTED)


#Class kiem soat gio hang cho khach hang
class ManageGioHang(APIView):
    serializer_class = DonHangSerializer

    permission_classes = (permissions.AllowAny, )

    # Tao lan dau tien
    def post(self, request):
        try: 
            idkhachhang = 10000
            while True:
                iddonhang = id_generator(size=5)
                if (Donhang.objects.filter(iddonhang = iddonhang).count() == 0):
                    break
            sotienthanhtoan = 0
            createday = datetime.date.today()
            trangthai = 'Checking'
            donhangtm = Donhang(iddonhang = iddonhang, idkhachhang = Khachhang(idkhachhang=idkhachhang), sotienthanhtoan=sotienthanhtoan,
                                createday = createday, trangthai = trangthai)
            donhangtm.save()
            return Response(DonHangSerializer(donhangtm).data, status=status.HTTP_201_CREATED)                  
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
            donhang_seria = DonHangSerializer(donhang)
            money = donhang_seria.data.get('sotienthanhtoan')

            khachhang = Khachhang.objects.get(idkhachhang = donhang_seria.data.get('idkhachhang'))
            nguoimua = khachhang.tenkhachhang

            danhsachgiay = Chitietdonhang.objects.filter(iddonhang = donhang.iddonhang)
            danhsachgiay_seria = ChitietDHSerializer(danhsachgiay, many = True)
            for group in danhsachgiay_seria.data:
                giay = Chitietgiay.objects.get(idgiay = group.get('idgiay'))
                giay_seria = ChitietGiaySerializer(giay)
                iddanhmuc = giay_seria.data.get('iddanhmuc')
                mausac = giay_seria.data.get('mausac')
                kichco = giay_seria.data.get('kichco')

                danhmucgiay = Danhmucgiay.objects.get(iddanhmuc = iddanhmuc)
                tendanhmuc = danhmucgiay.tendanhmuc
                loaigiay = danhmucgiay.loaigiay
                hangsanxuat = danhmucgiay.hangsanxuat
                giatien = danhmucgiay.giatien
                doituong = danhmucgiay.doituong

                idchitiet = group.get('idchitiet')
                soluong = group.get('soluong')

                list_giay.append(
                    {
                        'Mau giay' : 
                        {
                            "Ten" : tendanhmuc,
                            "Loai giay" : loaigiay,
                            "Hang san xuat" : hangsanxuat,
                            "Gia tien" : giatien,
                            "Doi tuong su dung" : doituong
                        },
                        'Thong tin chi tiet' : {
                            'Mau sac' : mausac,
                            'Kich co' : kichco,
                            'So luong' : soluong
                        },
                    }
                )
            return Response(
                {
                    'Thong tin don hang' : 
                        {
                            'Ten chu hang': nguoimua, 
                            'So tien thanh toan' : money
                        }
                    ,
                    'Danh sach mat hang cua quy khach hien tai': list_giay
                }
                ,status=status.HTTP_200_OK
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request):
        try:
            data = request.data
            iddonhang = data['iddonhang']
            action = data['action']
            donhang = Donhang.objects.get(iddonhang = iddonhang)
            serializer = DonHangSerializer(donhang)
            if action == 0:
                iddanhmuc = data['iddanhmuc']
                mausac = data['mausac']
                kichco = data['kichco']
                soluong = data['soluong']
                money = add_giay(serializer.data,iddanhmuc,soluong,mausac,kichco)
                donhang.sotienthanhtoan += money
                donhang.save()
            elif action == 1:
                idchitiet = data['idchitiet']
                money = remove_giay(serializer.data,idchitiet)
                donhang.sotienthanhtoan -= money
                donhang.save()
            elif action == 2:
                tenkhachhang = data['tenkhachhang']
                diachi = data['diachi']
                email = data['email']
                sdt = data['sdt']
                cofirm_donhang(serializer.data,tenkhachhang,diachi,email,sdt)
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


#Tra ve thong tin chi tiet ve giay cho khach hang
class GetDetailsGiay(APIView):
    serializer_class = ChitietGiaySerializer

    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        colour_list = []
        size_list = []

        try:
            data = request.data
            iddanhmuc = data['iddanhmuc']
            list_giay = Chitietgiay.objects.filter(iddanhmuc = iddanhmuc)
            list_giay_seria = self.serializer_class(list_giay, many = True)
            for group in list_giay_seria.data:
                giay = Chitietgiay.objects.get(idgiay = group.get('idgiay'))
                #Neu het hang , bo qua mau giay nay
                if giay.sotonkho == 0:
                    continue
                else:
                    colour = giay.mausac
                    size = giay.kichco
                    if not size_list.__contains__(size):
                        size_list.append(size)
                    if not colour_list.__contains__(colour):
                        colour_list.append(colour)
            danhmuc = Danhmucgiay.objects.get(iddanhmuc=iddanhmuc)
            serializer = DanhMucGiaySerializer(danhmuc)
            tendanhmuc = serializer.data.get('tendanhmuc')
            loaigiay = serializer.data.get('loaigiay')
            hangsanxuat = serializer.data.get('hangsanxuat')
            giatien = serializer.data.get('giatien')
            doituong = serializer.data.get('doituong')
            return JsonResponse(
                {
                    'Thong tin giay' : 
                    {
                        'tendanhmuc' : tendanhmuc,
                        'loaigiay' : loaigiay,
                        'hangsanxuat' : hangsanxuat,
                        'giatien' : giatien,
                        'doituong' : doituong
                    },
                    'List mau sac co': colour_list,
                    'List kich thuoc co' : size_list
                }, safe= False
                , status=status.HTTP_200_OK
            )          
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#Class kiem soat review khach hang
class ManageReview(APIView):

    serializer_class = ReviewSPSerializer

    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try: 
            data = request.data
            while True:
                idreview = id_generator(size=5)
                if (Reviewsanpham.objects.filter(idreview = idreview).count() == 0):
                    break
            idtaikhoan = data['idtaikhoan']
            iddanhmuc = data['iddanhmuc']
            comment = data['comment']
            createday = datetime.date.today()
            review = Reviewsanpham(idreview,idtaikhoan = TaikhoanKhachhang(idtaikhoan=idtaikhoan), idloaigiay= Danhmucgiay(iddanhmuc=iddanhmuc)
                                   ,comment=comment, createday=createday)
            review.save()
            return Response(
                    ReviewSPSerializer(review).data
                    ,status=status.HTTP_201_CREATED
            )         
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        try:
            list_review = []
            data = request.data
            iddanhmuc = data['iddanhmuc']
            review = Reviewsanpham.objects.filter(idloaigiay=iddanhmuc)
            serializer = self.serializer_class(review, many=True)
            for group in serializer.data:
                one = Reviewsanpham.objects.get(idreview = group.get('idreview'))
                host = TaikhoanKhachhang.objects.get(idtaikhoan = group.get('idtaikhoan'))
                
                tenkhach = host.username
                comment = one.comment

                list_review.append(
                    {
                        'Nguoi viet' : tenkhach,
                        'Noi dung' : comment
                    }
                )
            thongtin = Danhmucgiay.objects.get(iddanhmuc=iddanhmuc)
            name = thongtin.tendanhmuc
            return JsonResponse(
                {
                    'San pham' : name,
                    'Cac review san pham' : list_review
                }
                , safe= False
                , status = status.HTTP_200_OK
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request):
        try:
            data = request.data
            idreview = data['idreview']
            comment = data['comment']
            review = Reviewsanpham.objects.get(idreview = idreview)
            review.comment = comment
            review.save()
            return Response(
                {'Update success' : ReviewSPSerializer(review).data}
                ,status=status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        try:
            data = request.data
            idreview = data['idreview']
            review = Reviewsanpham.objects.get(idreview = idreview)
            review.delete()
            return Response(
                    {'Result': 'Delete successful'}, 
                    status= status.HTTP_202_ACCEPTED
                )   
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#Lay lich su mua hang cua khach cho server and client
class HistoryActivities(APIView):

    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        try: 
            list_muaban = []
            data = request.data
            idtaikhoan = data['idtaikhoan']
            taikhoan = TaikhoanKhachhang.objects.get(idtaikhoan=idtaikhoan)
            khachhang = taikhoan.idkhachhang
            danhsachdon = Donhang.objects.filter(idkhachhang = khachhang)
            danhsachdon_seria = DonHangSerializer(danhsachdon, many= True)
            for group in danhsachdon_seria.data:
                donhang = Donhang.objects.get(iddonhang = group.get('iddonhang'))
                money = donhang.sotienthanhtoan
                ngaythuchien = donhang.createday
                trangthai = donhang.trangthai
                list_muaban.append(
                    {
                            'Thanh toan' : money,
                            'Ngay thuc hien' : ngaythuchien,
                            'Tinh trang' : trangthai
                    }
                )
            return Response(
                {'Lich su mua ban': list_muaban}
                , status= status.HTTP_200_OK
            )   
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class ShowDetailsAccount(APIView):

    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        try:
            data = request.data
            idtaikhoan = data['idtaikhoan']
            taikhoan = TaikhoanKhachhang.objects.get(idtaikhoan = idtaikhoan)
            
            thongtin = Khachhang.objects.get(idkhachhang = taikhoan.idkhachhang)
            name = thongtin.tenkhachhang
            address = thongtin.diachi
            email = thongtin.email
            phonenumber = thongtin.sdt

            sex =  taikhoan.gioitinh
            brithday = taikhoan.ngaysinh
            diemtichluy = taikhoan.diemtichluy
            createday = taikhoan.ngaylaptk
            return Response(
                {
                    'Thong tin khach hang' : {
                        'Ten day du': name,
                        'Dia chi' : address,
                        'Email ' : email,
                        'So dien thoai' : phonenumber
                    },
                    'Thong tin tai khoan' : {
                        'Gioi tinh' : sex,
                        'Ngay sinh' : brithday,
                        'Diem tich luy' : diemtichluy,
                        'Ngay lap' : createday}
                }
                , status=status.HTTP_200_OK
            )
            
        except:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
