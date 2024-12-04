from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .models import SinhVien, GiangVien
from .models import UserAccount, UserAccountManager
from .models import LopHoc, ThanhVienLop
from .serializers import UserAccountSerializer
from .serializers import SinhVienSerializer, GiangVienSerializer
from .serializers import LopHocSerializer, ThanhVienLopSerializer
from django.contrib.auth import get_user_model
import traceback
import random, string
import datetime

User = get_user_model()

# Create your views here.
def is_valid_param(param) :
    return param != " " and param is not None and param != ""


def id_generator (size, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class ManageClassTeacher(APIView):

    permission_classes = (permissions.AllowAny, )

    #Create class
    def post(self, request, format=None):
        try:
            data = request.data
            user = request.user
            if (not user.is_teacher):
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            giangvien = data['idgiangvien']
            if GiangVien.objects.filter(idgiangvien=giangvien).count() == 0:
                return  Response(
                    {'error': 'Khong tim thay giang vien'}, 
                    status= status.HTTP_404_NOT_FOUND
                )
            else: 
                while True:
                    idlophoc = id_generator(size=6)
                    if (LopHoc.objects.filter(idlophoc = idlophoc).count() == 0):
                        break                      
                    
                tenlophoc = data['tenlophoc']
                mota = data['mota']
                cahoc = data['cahoc']
                ngayhoc = data['ngayhoc']
                kyhoc = data['kyhoc']
                maxstudent = data['sosinhvientoida']
                trangthai = 0

                
                lophoc = LopHoc(idlophoc = idlophoc, tenlophoc = tenlophoc, mota = mota, cahoc = cahoc, ngayhoc = ngayhoc, kyhoc = kyhoc, maxstudent = maxstudent, 
                                trangthai = trangthai, idgiangvien = GiangVien.objects.get(idgiangvien = giangvien))
                lophoc.save()
                
                return Response(
                    {"Da luu thong tin lop moi" : LopHocSerializer(lophoc).data},
                    status=status.HTTP_201_CREATED
                )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Get class list for teacher
    def get(self, request):
        try:
            user = request.user
            if (not user.is_teacher) or user.is_active == False:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            list_class = []
            user_id = user.id
            giangvien = GiangVien.objects.get(id = user_id)
            idgiangvien = giangvien.idgiangvien
            tengiangvien = giangvien.tengiangvien
            tenchucvu = giangvien.tenchucvu

            lopgiangday = LopHoc.objects.filter(idgiangvien = idgiangvien)
            lopgiangday_seria = LopHocSerializer(lopgiangday, many = True)
            for group in lopgiangday_seria.data :
                idlophoc = group.get('idlophoc')
                tenlophoc = group.get('tenlophoc')
                mota = group.get('mota')
                cahoc = group.get('cahoc')
                ngayhoc = group.get('ngayhoc')
                kyhoc = group.get('kyhoc')
                maxstudent = group.get('maxstudent')
                trangthai = group.get('trangthai')

                list_class.append(
                    {
                        "Ma lop" : idlophoc,
                        "Ten lop hoc" : tenlophoc,
                        "Mo ta" : mota,
                        "Gio bat dau" : cahoc,
                        "Ngay hoc trong tuan" : ngayhoc,
                        "Ky hoc" : kyhoc,
                        "So sinh vien toi da" : maxstudent,
                        "Trang thai" : trangthai,
                    }
                )

            return Response(
                {
                    'Thong tin giang vien' : 
                    {
                        "Ten giang vien" : tengiangvien,
                        "Ten chuc vu" : tenchucvu
                    },
                    'Danh sach lop giang day': list_class
                }, 
                status= status.HTTP_200_OK
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong!'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Edit class
    def put(self, request):
        try: 
            user= request.user
            if (not user.is_teacher):
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data=request.data
            idlophoc = data['idlophoc']
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return JsonResponse(
                    {'error': 'No matching'}
                    ,safe=False 
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            idgiangvien =  data['idgiangvien']
            if GiangVien.objects.filter(idgiangvien = idgiangvien).count() == 0:
                return  Response(
                    {'error': 'Khong tim thay giang vien'}, 
                    status= status.HTTP_404_NOT_FOUND
                )
            tenlophoc = data['tenlophoc']
            mota = data['mota']
            cahoc = data['cahoc']
            ngayhoc = data['ngayhoc']
            kyhoc = data['kyhoc']
            maxstudent = data['sosinhvientoida']
            trangthai = data['trangthai']

            lophoc = LopHoc.objects.get(idlophoc = idlophoc)
            lophoc.tenlophoc = tenlophoc
            lophoc.mota = mota
            lophoc.cahoc = cahoc
            lophoc.ngayhoc = ngayhoc
            lophoc.kyhoc = kyhoc
            lophoc.maxstudent = maxstudent
            lophoc.trangthai = trangthai
            lophoc.save()

            lophoc_seria = LopHocSerializer(lophoc)

            return Response(
                {'Update success': lophoc_seria.data},
                status= status.HTTP_202_ACCEPTED
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Delete class
    def delete(self, request):
        try: 
            user= request.user
            if (not user.is_teacher):
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data=request.data
            idlophoc = data['idlophoc']
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return JsonResponse(
                    {'error': 'No matching'}
                    ,safe=False 
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            else:
                list_thanhvien = ThanhVienLop.objects.filter(idlophoc = idlophoc)
                if list_thanhvien.count() != 0:
                    list_thanhvien_seria = ThanhVienLopSerializer(list_thanhvien, many = True)
                    for group in list_thanhvien_seria.data:
                        thanhvien = ThanhVienLop.objects.get(idthanhvien = group.get('idthanhvien'))
                        thanhvien.delete()
                lophoc = LopHoc.objects.get(idlophoc = idlophoc)
                lophoc.delete()

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
        

class ManageClassMember(APIView):

    permission_classes = (permissions.AllowAny, )
    
    #Sign in class
    def post(self, request, format=None):
        try:
            user = request.user
            if (user.is_teacher):
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data
            sinhvien =  SinhVien.objects.get(id = user.id)
            idlophoc = data['idlophoc']
            lophoc = LopHoc.objects.get(idlophoc = idlophoc)
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return  Response(
                    {'error': 'Khong tim thay lop hoc'}, 
                    status= status.HTTP_404_NOT_FOUND
                )
            elif lophoc.trangthai != 0:
                return  Response(
                    {'error': 'Lớp đã quá thời hạn đăng ký'}, 
                    status= status.HTTP_404_NOT_FOUND
                )

            while True:
                idthanhvien = id_generator(size=6)
                if (ThanhVienLop.objects.filter(idthanhvien = idthanhvien).count() == 0):    
                    break                      
                
            thanhvienlop = ThanhVienLop(idthanhvien = idthanhvien, tinhtranghoc = 0, idsinhvien = sinhvien, idlophoc = lophoc)
            thanhvienlop.save()
                
            return Response(
                {"Da dang ky vao lop thanh cong" : ThanhVienLopSerializer(thanhvienlop).data},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Get class info
    def get(self, request):
        try:
            list_class_member = []
            data = request.data

            idlophoc = data['idlophoc']
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return  Response(
                    {'error': 'Khong tim thay lop hoc'}, 
                    status= status.HTTP_404_NOT_FOUND
                )
            
            lopgiangday = LopHoc.objects.get(idlophoc = idlophoc)
            lopgiangday_seria = LopHocSerializer(lopgiangday)
            idgiangvien = lopgiangday_seria.data.get('idgiangvien')
            tengiangvien = GiangVien.objects.get(idgiangvien = idgiangvien).tengiangvien

            tenlophoc = lopgiangday.tenlophoc
            mota = lopgiangday.mota
            cahoc = lopgiangday.cahoc
            ngayhoc = lopgiangday.ngayhoc
            kyhoc = lopgiangday.kyhoc
            trangthai = lopgiangday.trangthai

            thanhvienlop = ThanhVienLop.objects.filter(idlophoc = idlophoc)
            thanhvien_seria = ThanhVienLopSerializer(thanhvienlop, many = True)
            
            count = 0
            
            for group in thanhvien_seria.data :
                idsinhvien = group.get('idsinhvien')
                sinhvien = SinhVien.objects.get(idsinhvien = idsinhvien)
                tensinhvien = sinhvien.tensinhvien
                sdt = sinhvien.sdt

                tinhtranghoc = group.get('tinhtranghoc')

                list_class_member.append(
                    {
                        "Ma sinh vien" : idsinhvien,
                        "Ten sinh vien" : tensinhvien,
                        "So dien thoai" : sdt,
                        "Tinh trang hoc" : tinhtranghoc
                    }
                )

                count = count + 1

            return Response(
                {
                    'Thong tin chi tiet' : {
                        "Ma lop hoc " : idlophoc,
                        "Ten lop hoc" : tenlophoc,
                        "Ten giang vien" : tengiangvien,
                        "Mo ta" : mota,
                        "Gio bat dau" : cahoc,
                        "Ngay hoc" : ngayhoc,
                        "Ky hoc" : kyhoc,
                        "So sinh vien " : count,
                        "Trang thai lop" : trangthai 
                    },
                    'Danh sach thanhvien': list_class_member
                }, 
                status= status.HTTP_200_OK
            )
            
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong!'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Edit class member
    def put(self, request):
        try: 
            user= request.user
            if (not user.is_teacher) or user.is_active == False:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data=request.data
            idthanhvien = data['idthanhvien']
            if ThanhVienLop.objects.filter(idthanhvien = idthanhvien).count() == 0:
                return Response(
                    {'error': 'No matching data'}
                    ,status= status.HTTP_404_NOT_FOUND
                )
            
            tinhtranghoc = data['tinhtranghoc']
            if tinhtranghoc < 0 or tinhtranghoc > 3:
                return Response(
                    {'error': 'Mismatch data. Please check with the admin'}
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            
            thanhvienlop = ThanhVienLop.objects.get(idthanhvien = idthanhvien)
            thanhvienlop.tinhtranghoc = tinhtranghoc
            thanhvienlop.save()

            return Response(
                {'Update success'}
                ,status= status.HTTP_202_ACCEPTED
            )
        
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Delete class member
    def delete(self, request):
        try: 
            user= request.user
            if (not user.is_teacher) or user.is_active == False:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data=request.data
            idsinhvien = data['idsinhvien']
            idlophoc = data['idlophoc']
            if SinhVien.objects.filter(idsinhvien = idsinhvien).count() == 0 or LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return JsonResponse(
                    {'error': 'No matching data'}
                    ,safe=False 
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            else:
                thanhvienlop = ThanhVienLop.objects.get(idsinhvien = idsinhvien, idlophoc = idlophoc)
                thanhvienlop.delete()

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
        

class ManageClassStudent(APIView):

    permission_classes = (permissions.AllowAny, )

    #Get class list for student
    def get(self, request):
        try:
            user = request.user
            if (user.is_teacher):
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            list_class = []
            user_id = user.id
            sinhvien = SinhVien.objects.get(id = user_id)
            sinhvien_id = sinhvien.idsinhvien

            lopdangky = ThanhVienLop.objects.filter(idsinhvien = sinhvien_id)
            lopdangky_seria = ThanhVienLopSerializer(lopdangky, many = True)
            for group in lopdangky_seria.data :
                idlophoc = group.get('idlophoc')
                tinhtranghoc = group.get('tinhtranghoc')
                lophoc = LopHoc.objects.get(idlophoc = idlophoc)
                tenlophoc = lophoc.tenlophoc
                mota = lophoc.mota
                cahoc = lophoc.cahoc
                ngayhoc = lophoc.ngayhoc
                kyhoc = lophoc.kyhoc

                lopgiangday_seria = LopHocSerializer(lophoc)
                idgiangvien = lopgiangday_seria.data.get('idgiangvien')
                tengiangvien = GiangVien.objects.get(idgiangvien = idgiangvien).tengiangvien

                list_class.append(
                    {
                        "Ma lop" : idlophoc,
                        "Ten lop hoc" : tenlophoc,
                        "Ten giang vien" : tengiangvien,
                        "Mo ta" : mota,
                        "Gio bat dau" : cahoc,
                        "Ngay hoc" : ngayhoc,
                        "Ky hoc" : kyhoc,
                        "Trang thai" : tinhtranghoc
                    }
                )

            return Response(
                {'Danh sach lop dang ky': list_class}, 
                status= status.HTTP_200_OK
            )
            
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong!'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )