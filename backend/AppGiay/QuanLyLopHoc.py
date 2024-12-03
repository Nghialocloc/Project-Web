from rest_framework import generics, permissions, status, authentication
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
            user = request.user
            if (not user.is_teacher) or user.is_active == False:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = LopHocSerializer(data=request.data)
            giangvien = serializer.data.get('idgiangvien')
            if GiangVien.objects.filter(idgiangvien=giangvien).count() == 0:
                return  Response(
                        {'error': 'Khong tim thay giang vien'}, 
                        status= status.HTTP_404_NOT_FOUND
                    )
            else: 
                if serializer.is_valid():
                    while True:
                        idlophoc = id_generator(size=6)
                        if (LopHoc.objects.filter(idlophoc = idlophoc).count() == 0):
                            break                      
                    
                    tenlophoc = serializer.data.get('tenlophoc') 
                    mota = serializer.data.get('mota')
                    cahoc = serializer.data.get('cahoc')
                    ngayhoc = serializer.data.get('ngayhoc')
                    kyhoc = serializer.data.get('kyhoc')
                    maxstudent = serializer.data.get('sosinhvientoida')
                    trangthai = 0

                
                    lophoc = LopHoc(idlophoc = idlophoc, tenlophoc = tenlophoc, mota = mota, cahoc = cahoc, 
                                    ngayhoc = ngayhoc, kyhoc = kyhoc, maxstudent = maxstudent, trangthai = trangthai, idgiangvien = giangvien)
                    lophoc.save()
                
                    return Response(
                        {"Da luu thong tin lop moi" : LopHocSerializer(lophoc).data},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return  Response(
                        {'error': 'Du lieu dau vao bi thieu hoac sai'}, 
                        status= status.HTTP_400_BAD_REQUEST
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
            user_id = user.data['id']
            giangvien = GiangVien.objects.get(user_id = user_id)
            giangvien_id = giangvien.idgiangvien

            lopgiangday = LopHoc.objects.filter(idgiangvien = giangvien_id)
            lopgiangday_seria = LopHocSerializer(data = lopgiangday, many = True)
            if lopgiangday_seria.is_valid():
                for group in lopgiangday_seria :
                    idlophoc = group.data.get('idlophoc')
                    tenlophoc = group.data.get('tenlophoc')
                    mota = group.data.get('mota')
                    cahoc = group.data.get('cahoc')
                    ngayhoc = group.data.get('ngayhoc')
                    kyhoc = group.data.get('kyhoc')
                    maxstudent = group.data.get('maxstudent')
                    trangthai = group.data.get('status')

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
                    {'Danh sach lop giang day': list_class}, 
                    status= status.HTTP_200_OK
                )
            else:
                return Response(
                    {'Du lieu gap su co'}, 
                    status= status.HTTP_400_BAD_REQUEST
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
            if (not user.is_teacher) or user.is_active == False:
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
            return JsonResponse(
                {'Update success'}
                , safe=False 
                ,status= status.HTTP_202_ACCEPTED
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
            if (not user.is_teacher) or user.is_active == False:
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
            if (user.is_teacher) or user.is_active == False:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )

            data=request.data
            sinhvien =  SinhVien.objects.get(id = user.id)
            idlophoc = data['idlophoc']
            lophoc = LopHoc.objects.get(idlophoc = idlophoc)
            if LopHoc.objects.filter(idlophoc = lophoc).count() == 0:
                return  Response(
                    {'error': 'Khong tim thay lop hoc'}, 
                    status= status.HTTP_404_NOT_FOUND
                )
            elif lophoc.trangthai != 0:
                return  Response(
                    {'error': 'Lớp đã quá thời hạn đăng ký'}, 
                    status= status.HTTP_404_NOT_FOUND
                )

            serializer = ThanhVienLopSerializer(data=request.data)
            if serializer.is_valid():
                while True:
                    idthanhvien = id_generator(size=6)
                    if (ThanhVienLop.objects.filter(idthanhvien = idthanhvien).count() == 0):    
                        break                      
                
                thanhvienlop = ThanhVienLop(idthanhvien = idthanhvien, tinhtranghoc = 0, idsinhvien = sinhvien, idlophoc = idlophoc)
                thanhvienlop.save()
                
                return Response(
                    {"Da dang ky vao lop thanh cong" : ThanhVienLopSerializer(thanhvienlop).data},
                    status=status.HTTP_201_CREATED
                )
            else:     
                return  Response(
                    {'error': 'Du lieu dau vao bi thieu hoac sai'}, 
                    status= status.HTTP_400_BAD_REQUEST
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
            tenlophoc = lopgiangday.tenlophoc
            mota = lopgiangday.mota
            cahoc = lopgiangday.cahoc
            ngayhoc = lopgiangday.ngayhoc
            kyhoc = lopgiangday.kyhoc
            trangthai = lopgiangday.trangthai

            count = 0
            tengiangvien = GiangVien.objects.get(idgiangvien = lopgiangday.idgiangvien)

            thanhvienlop = ThanhVienLop.objects.filter(idlophoc = idlophoc)
            thanhvien_seria = ThanhVienLopSerializer(data = thanhvienlop, many = True)
            if thanhvien_seria.is_valid():
                for group in thanhvien_seria :
                    idsinhvien = group.data.get('idsinhvien')
                    sinhvien = SinhVien.objects.get(idsinhvien = idsinhvien)
                    tensinhvien = sinhvien.tensinhvien
                    sdt = sinhvien.sdt

                    tinhtranghoc = group.data.get('tinhtranghoc')

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
            else:
                return Response(
                    {'Du lieu gap su co'}, 
                    status= status.HTTP_400_BAD_REQUEST
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
                return JsonResponse(
                    {'error': 'No matching data'}
                    ,safe=False 
                    ,status= status.HTTP_204_NO_CONTENT
                )
            
            tinhtranghoc = data['tinhtranghoc']
            if tinhtranghoc < 0 or tinhtranghoc > 3:
                return JsonResponse(
                    {'error': 'Mismatch data. Please check with the admin'}
                    ,safe=False 
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            
            thanhvienlop = ThanhVienLop.objects.get(idthanhvien = idthanhvien)
            thanhvienlop.tinhtranghoc = tinhtranghoc
            thanhvienlop.save()

            return JsonResponse(
                {'Update success'}
                , safe=False 
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
            if (user.is_teacher) or user.is_active == False:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            list_class = []
            user_id = user.data['id']
            sinhvien = SinhVien.objects.get(user_id = user_id)
            sinhvien_id = sinhvien.idsinhvien

            lopdangky = ThanhVienLop.objects.filter(idsinhvien = sinhvien_id)
            lopdangky_seria = ThanhVienLopSerializer(data = lopdangky, many = True)
            if lopdangky_seria.is_valid():
                for group in lopdangky_seria :
                    idlophoc = group.data.get('idlophoc')
                    tinhtranghoc = group.data.get('tinhtranghoc')
                    lophoc = LopHoc.objects.get(idlophoc = idlophoc)
                    tenlophoc = lophoc.tenlophoc
                    mota = lophoc.mota
                    cahoc = lophoc.cahoc
                    ngayhoc = lophoc.ngayhoc
                    kyhoc = lophoc.kyhoc

                    tengiangvien = GiangVien.objects.get(idgiangvien = lophoc.idgiangvien)

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
            else:
                return Response(
                    {'Du lieu gap su co'}, 
                    status= status.HTTP_400_BAD_REQUEST
                )
            
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong!'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )