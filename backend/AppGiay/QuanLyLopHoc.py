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
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            giangvien = data['idgiangvien']
            if GiangVien.objects.filter(idgiangvien=giangvien).count() == 0:
                return  Response(
                    {
                        'code' : 1004,
                        'message': 'Teacher id not found'
                    }, 
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
                start_day = data['batdau']
                end_day = data['ketthuc']

                thoigiangui = datetime.datetime.now()
                
                if is_valid_param(tenlophoc) == False or len(tenlophoc) > 50:
                    return  Response(
                        {
                            'code' : 1004,
                            'message': 'Class name is invalid. Please input name again.'
                        }, 
                        status= status.HTTP_404_NOT_FOUND
                    )
                
                if is_valid_param(maxstudent) == False or maxstudent > 200:
                    return  Response(
                        {
                            'code' : 1004,
                            'message': 'Max student is invalid or bigger than 200. Please input again.'
                        }, 
                        status= status.HTTP_404_NOT_FOUND
                    )
                
                if start_day > end_day:
                    return  Response(
                        {
                            'code' : 1004,
                            'message': 'The start day must before the end day.'
                        }, 
                        status= status.HTTP_406_NOT_ACCEPTABLE
                    )
                
                if start_day < str(thoigiangui):
                    return  Response(
                        {
                            'code' : 1004,
                            'message': 'The start day must not in the past.'
                        }, 
                        status= status.HTTP_406_NOT_ACCEPTABLE
                    )

                lophoc = LopHoc(idlophoc = idlophoc, tenlophoc = tenlophoc, mota = mota, cahoc = cahoc, ngayhoc = ngayhoc, kyhoc = kyhoc, maxstudent = maxstudent, 
                                trangthai = trangthai, start_day = start_day, end_day = end_day,idgiangvien = GiangVien.objects.get(idgiangvien = giangvien))
                lophoc.save()
                
                return Response(
                    {
                        "code" : 1000,
                        "message" : "OK"
                    },
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
            if (not user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
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
                trangthai = group.get('trangthai')
                ngaybatdau = group.get('start_day')
                ngayketthuc = group.get('end_day')

                studentcount = ThanhVienLop.objects.filter(idlophoc = idlophoc).count()

                list_class.append(
                    {
                        "Ma lop" : idlophoc,
                        "Ten lop hoc" : tenlophoc,
                        "Mo ta" : mota,
                        "Gio bat dau" : cahoc,
                        "Ngay hoc trong tuan" : ngayhoc,
                        "Ky hoc" : kyhoc,
                        "So luong sinh vien" : studentcount,
                        "Trang thai" : trangthai,
                        "Ngay bat dau" : ngaybatdau,
                        "Ngay ket thuc" : ngayketthuc,
                    }
                )

            return Response(
                {
                    'code' : "1000",
                    'message' : "OK",
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
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data=request.data
            idlophoc = data['idlophoc']
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return JsonResponse(
                    {
                        'code' : 1004,
                        'message': 'Class not found. Please try again.'
                    }
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            
            tenlophoc = data['tenlophoc']
            mota = data['mota']
            maxstudent = data['sosinhvientoida']
            trangthai = data['trangthai']
            ngaybatdau = data['ngaybatdau']
            ngayketthuc = data['ngayketthuc']

            lophoc = LopHoc.objects.get(idlophoc = idlophoc)

            if is_valid_param(tenlophoc) == True:
                lophoc.tenlophoc = tenlophoc

            lophoc.mota = mota
            
            if is_valid_param(maxstudent) == True:
                lophoc.maxstudent = maxstudent

            if is_valid_param(trangthai) == True:
                lophoc.trangthai = trangthai

            if is_valid_param(ngaybatdau) == True:
                lophoc.start_day = ngaybatdau

            if is_valid_param(ngayketthuc) == True:
                lophoc.end_day = ngayketthuc
            
            lophoc.save()

            return Response(
                {
                    'code' : 1000,
                    'message': "Update success"
                },
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
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data=request.data
            idlophoc = data['idlophoc']
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return JsonResponse(
                    {
                        'code' : 1004,
                        'message': 'Class not found. Please try again.'
                    }
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
                    {
                        'code' : 1000,
                        'message': 'Ok.'
                    }
                    ,status= status.HTTP_200_OK
                ) 

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class ManageClassStudent(APIView):

    permission_classes = (permissions.AllowAny, )
    
    #Sign in class
    def post(self, request, format=None):
        try:
            user = request.user
            if (user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data
            sinhvien =  SinhVien.objects.get(id = user.id)
            idlophoc = data['idlophoc']
            lophoc = LopHoc.objects.get(idlophoc = idlophoc)
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return  Response(
                    {
                        'code' : 1004,
                        'message': 'Class not found. Please check input'
                    }, 
                    status= status.HTTP_404_NOT_FOUND
                )
            elif lophoc.trangthai != 0:
                return  Response(
                    {
                        'code' : 1004,
                        'message': 'Lớp đã quá thời hạn đăng ký'
                    }, 
                    status= status.HTTP_404_NOT_FOUND
                )

            while True:
                idthanhvien = id_generator(size=6)
                if (ThanhVienLop.objects.filter(idthanhvien = idthanhvien).count() == 0):    
                    break                      
                
            thanhvienlop = ThanhVienLop(idthanhvien = idthanhvien, tinhtranghoc = 0, idsinhvien = sinhvien, idlophoc = lophoc)
            thanhvienlop.save()
                
            return Response(
                {
                    'code' : 1000,
                    'message' : "Da dang ky vao lop thanh cong",
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Get class list for student
    def get(self, request):
        try:
            user = request.user
            if (user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
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
                ngaybatdau = lophoc.start_day
                ngayketthuc = lophoc.end_day
                
                studentcount = ThanhVienLop.objects.filter(idlophoc = idlophoc).count()

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
                        "So luong sinh vien" : studentcount,
                        "Trang thai" : tinhtranghoc,
                        "Ngay bat dau" : ngaybatdau,
                        "Ngay ket thuc" : ngayketthuc,
                    }
                )

            return Response(
                {
                    'code' : 1000,
                    'message' : "OK",
                    'Danh sach lop dang ky': list_class
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
            if (not user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data=request.data
            idthanhvien = data['idthanhvien']
            if ThanhVienLop.objects.filter(idthanhvien = idthanhvien).count() == 0:
                return Response(
                    {
                        'code' : 1004,
                        'message': 'Member not found.' 
                    }
                    ,status= status.HTTP_404_NOT_FOUND
                )
            
            tinhtranghoc = data['tinhtranghoc']
            if tinhtranghoc < 0 or tinhtranghoc > 3:
                return Response(
                    {
                        'code' : 1004,
                        'message': 'Input invalid. Please try again.' 
                    }
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            
            thanhvienlop = ThanhVienLop.objects.get(idthanhvien = idthanhvien)
            thanhvienlop.tinhtranghoc = tinhtranghoc
            thanhvienlop.save()

            return Response(
                {
                    'code' : 1000,
                    'message': 'OK' 
                }
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
            if (not user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data=request.data
            idsinhvien = data['idsinhvien']
            idlophoc = data['idlophoc']
            if SinhVien.objects.filter(idsinhvien = idsinhvien).count() == 0 or LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return JsonResponse(
                    {
                        'code' : 1004,
                        'message': 'Member not found.' 
                    }
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            else:
                thanhvienlop = ThanhVienLop.objects.get(idsinhvien = idsinhvien, idlophoc = idlophoc)
                thanhvienlop.delete()

                return Response(
                    {
                        'code' : 1000,
                        'message': 'OK' 
                    }
                    ,status= status.HTTP_202_ACCEPTED
                )        

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
     

class GetClassInfo(APIView):

    permission_classes = (permissions.AllowAny, )

    #Get class info
    def get(self, request):
        try:
            list_class_member = []
            data = request.data

            idlophoc = data['idlophoc']
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return  Response(
                    {
                        'code' : 1004,
                        'message': 'Class not found. Please check input again'
                    }, 
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
            ngaybatdau = lopgiangday.start_day
            ngayketthuc = lopgiangday.end_day

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
                    'code' : 1000,
                    'message' : "OK",
                    'Thong tin chi tiet' : {
                        "Ma lop hoc " : idlophoc,
                        "Ten lop hoc" : tenlophoc,
                        "Ten giang vien" : tengiangvien,
                        "Mo ta" : mota,
                        "Gio bat dau" : cahoc,
                        "Ngay hoc" : ngayhoc,
                        "Ky hoc" : kyhoc,
                        "So sinh vien " : count,
                        "Trang thai lop" : trangthai,
                        "Ngay bat dau" : ngaybatdau,
                        "Ngay ket thuc" : ngayketthuc,

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