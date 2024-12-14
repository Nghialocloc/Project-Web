from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SinhVien, GiangVien
from .models import LopHoc, ThanhVienLop, DonXinNghi
from .models import BuoiHoc, DiemDanh
from .serializers import UserAccountSerializer
from .serializers import LopHocSerializer, ThanhVienLopSerializer, DonXinNghiSerializer
from .serializers import BuoiHocSerializer, DiemDanhSerializer
from django.contrib.auth import get_user_model
import traceback
import random, string
import datetime

User = get_user_model()

def is_valid_param(param) :
    return param != " " and param is not None and param != ""


def id_generator (size, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def new_attendance(idlophoc, ngaydienra):

    while True:
        idbuoihoc = id_generator(size=6)
        if (BuoiHoc.objects.filter(idbuoihoc= idbuoihoc ).count() == 0):
            break
    
    buoihoc = BuoiHoc(idbuoihoc=idbuoihoc, idlophoc=idlophoc, ngaydienra=ngaydienra)
    buoihoc.save()
    
    return buoihoc


class ManageAttendanceClass(APIView):

    permission_classes = (permissions.AllowAny, )

    #Create attendance
    def post(self, request, format=None):
        try:
            data = request.data
            user = request.user
            if (not user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            idlophoc = data['idlophoc']
            ngaydienra = data['ngayhoc']
            attendance_list = data['attendance_list', []]
            
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return  Response(
                    {
                        'code' : 1004,
                        'message': 'Class not found. Please check id input' 
                    }, 
                    status= status.HTTP_404_NOT_FOUND
                )
            
            lophoc = LopHoc.objects.get(idlophoc = idlophoc)
            lophoc_seria = LopHocSerializer(lophoc)
            idgiangvien = lophoc_seria.data.get('idgiangvien')

            giangvien = GiangVien.objects.get(id = user.id)
            if giangvien.idgiangvien != idgiangvien:
                return Response(
                    {
                        'code' : 1009,
                        'message': 'This teacher doesn"t manage this class and have necessary permission' 
                    }, 
                    status= status.HTTP_403_FORBIDDEN
                )
            
            thoigiangui = datetime.datetime.now()
            if ngaydienra < str(thoigiangui):
                return Response(
                        {
                            'code' : 1004,
                            'message': "Attendance day had passed. Please input again."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            else:
                buoihoc = new_attendance(idlophoc= idlophoc, ngaydienra= ngaydienra)
                member = ThanhVienLop.objects.filter(idlophoc = idlophoc)
                member_seria = ThanhVienLopSerializer(member, many = True)
                
                for group in member_seria.data:
                    idsinhvien = group.get('idsinhvien')

                    while True:
                        iddiemdanh = id_generator(size=8)
                        if (DiemDanh.objects.filter(iddiemdanh = iddiemdanh).count() == 0):
                            break
                    
                    if idsinhvien in attendance_list:
                        trangthaidiemdanh = 3
                    else:
                        trangthaidiemdanh = 0
                    
                    thoigiandiemdanh = datetime.datetime.now()

                    diemdanh = DiemDanh(iddiemdanh = iddiemdanh, idbuoihoc = buoihoc.idbuoihoc, idsinhvien = idsinhvien, 
                                        trangthaidiemdanh = trangthaidiemdanh, thoigiandiemdanh = thoigiandiemdanh)
                    diemdanh.save()

                return Response(
                    {
                        'code': 1000,
                        'meassage': "OK"
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Edit attendance
    def put(self, request):
        try: 
            user= request.user
            if (not user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data=request.data
            iddiemdanh = data['iddiemdanh']
            if DiemDanh.objects.filter(iddiemdanh = iddiemdanh).count() == 0:
                return Response(
                    {
                        'code' : 1005,
                        'message': 'id attendance not found. Please check input again.' 
                    }
                    ,status= status.HTTP_404_NOT_FOUND
                )

            status = data['status']
            thoigianphanhoi = datetime.datetime.now()

            diemdanh = DiemDanh.objects.get(iddiemdanh = iddiemdanh)
            diemdanh_seria = DiemDanhSerializer(diemdanh)
            idbuoihoc = diemdanh_seria.data.get('idbuoihoc')

            buoihoc = BuoiHoc.objects.get(idbuoihoc = idbuoihoc)
            buoihoc_seria = BuoiHocSerializer(buoihoc)
            idlophoc = buoihoc_seria.data.get('idlophoc')

            lophoc = LopHoc.objects.get(idlophoc = idlophoc)
            lophoc_seria = LopHocSerializer(lophoc)
            idgiangvien = lophoc_seria.data.get('idgiangvien')

            giangvien = GiangVien.objects.get(id = user.id)
            if giangvien.idgiangvien != idgiangvien:
                return Response(
                    {
                        'code' : 1009,
                        'message': 'This teacher doesn"t manage this class and have necessary permission' 
                    }, 
                    status= status.HTTP_403_FORBIDDEN
                )

            diemdanh.trangthaidiemdanh = status
            diemdanh.thoigiandiemdanh = thoigianphanhoi
            diemdanh.save()

            diemdanh_seria = DiemDanhSerializer(diemdanh)

            return Response(
                {
                    'code' : 1000,
                    'message': 'OK',
                    'Thong tin sau khi sua' : diemdanh_seria.data
                }
                ,status= status.HTTP_202_ACCEPTED
            )
        
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Get attendance list for teacher
    def get(self, request):
        try:
            user = request.user
            if (not user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            list_attendance = []
            
            data = request.data
            idlophoc = data['idlophoc']
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return Response(
                    {
                        'code' : 1004,
                        'message': 'Class not found. Please try again.' 
                    }
                    ,status= status.HTTP_400_BAD_REQUEST
                )      
            lophoc  = LopHoc.objects.get(idlophoc = idlophoc)
            tenlophoc = lophoc.tenlophoc
            
            ngaydienra = data['date']
            if BuoiHoc.objects.filter(idlophoc = idlophoc, ngaydienra = ngaydienra).count() == 0:
                return Response(
                    {
                        'code' : 1004,
                        'message': 'There are no attendance in the class that day. Please check input again.' 
                    }
                    ,status= status.HTTP_400_BAD_REQUEST
                )      

            buoihoc = BuoiHoc.objects.get(idlophoc = idlophoc, ngaydienra = ngaydienra)
            buoihoc_seria = BuoiHocSerializer(buoihoc)
            idbuoihoc = buoihoc_seria.data.get('idbuoihoc')

            diemdanh = DiemDanh.objects.filter(idbuoihoc = idbuoihoc)
            diemdanh_seria = DiemDanhSerializer(diemdanh, many = True)
            for group in diemdanh_seria.data :
                idsinhvien = group.get('idsinhvien')
                trangthaidiemdanh = group.get('trangthaidiemdanh')
                thoigiandiemdanh = group.get('thoigiandiemdanh')
                sinhvien = SinhVien.objects.get(idsinhvien = idsinhvien)
                tensinhvien = sinhvien.tensinhvien

                list_attendance.append(
                    {
                        "Id sinh vien" : idsinhvien,
                        "Ten sinh vien" : tensinhvien,
                        "Trang thai" : trangthaidiemdanh,
                        "Thoi gian diem danh" : thoigiandiemdanh,
                    }   
                )

            return Response(
                {
                    'code' : 1000,
                    'message' : "OK",
                    'Thong tin lop hoc' : 
                    {
                        "Id lop hoc" : idlophoc,
                        "Ten lop hoc" : tenlophoc
                    },
                    'Ngau diem danh' : ngaydienra,
                    'Danh sach diem danh': list_attendance
                }, 
                status= status.HTTP_200_OK
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong!'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetAttendanceRecord(APIView):

    permission_classes = (permissions.AllowAny, )

    