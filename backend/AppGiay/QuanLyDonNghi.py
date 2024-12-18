from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SinhVien, GiangVien
from .models import LopHoc, ThanhVienLop, DonXinNghi
from .serializers import UserAccountSerializer
from .serializers import LopHocSerializer, ThanhVienLopSerializer, DonXinNghiSerializer
from django.contrib.auth import get_user_model
import traceback
import random, string
import datetime
from django.utils import timezone

User = get_user_model()

def get_member_id(sinhvien, lophoc):
    thanhvien = ThanhVienLop.objects.get(idsinhvien = sinhvien, idlophoc = lophoc)
    return thanhvien.idthanhvien


def is_valid_param(param) :
    return param != " " and param is not None and param != ""


def is_past_due(self):
    return datetime.date.today() > self


def id_generator (size, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class ManageAbsenceForm(APIView):

    permission_classes = (permissions.AllowAny, )

    #Create form
    def post(self, request, format=None):
        try:
            data = request.data
            user = request.user
            if (user.is_teacher):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            sinhvien = SinhVien.objects.get(id = user.id)
            idsinhvien = sinhvien.idsinhvien
            idlophoc = data['idlophoc']
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return  Response(
                    {
                        'code' : 1004,
                        'message': 'Class not found. Please check id input' 
                    }, 
                    status= status.HTTP_404_NOT_FOUND
                )
            
            else: 
                while True:
                    iddon = id_generator(size=8)
                    if (DonXinNghi.objects.filter(iddon = iddon).count() == 0):
                        break                      
                
                idthanhvien = get_member_id(idsinhvien, idlophoc)
                ngayxinnghi = data['ngayxinnghi']
                lydo = data['lydo']
                trangthai = 0
                thoigiangui = timezone.now()

                if ngayxinnghi < str(thoigiangui):
                    return Response(
                        {
                            'code' : 1004,
                            'message': "Absence day had passed. Please input again."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                donnghi = DonXinNghi(iddon = iddon, idthanhvien = ThanhVienLop.objects.get(idthanhvien = idthanhvien), ngayxinnghi = ngayxinnghi, 
                                     lydo = lydo, trangthai = trangthai, thoigiangui = thoigiangui)
                donnghi.save()
                
                return Response(
                    {
                        'code': 1000,
                        'meassage': "OK"
                    },
                    status=status.HTTP_201_CREATED
                )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    #Edit form
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
            iddon = data['iddon']
            if iddon or (not is_valid_param(iddon)):
                return Response(
                    {
                        'code' : 1004,
                        'message': 'Invaild id. Please check input again.' 
                    }
                    ,status= status.HTTP_400_BAD_REQUEST
                )

            if DonXinNghi.objects.filter(iddon = iddon).count() == 0:
                return Response(
                    {
                        'code' : 1004,
                        'message': 'Form not found. Please check input again.' 
                    }
                    ,status= status.HTTP_404_NOT_FOUND
                )

            trangthai = data['trangthai']
            if trangthai < 0 or trangthai > 3:
                return Response(
                    {
                        'code' : 1005,
                        'message': 'Status is out of bound. Please check input again.' 
                    }
                    ,status= status.HTTP_404_NOT_FOUND
                )
            
            thoigianphanhoi = timezone.now()
            donnghi = DonXinNghi.objects.get(iddon = iddon)
            
            donnghi_seria = DonXinNghiSerializer(donnghi)
            idthanhvien = donnghi_seria.data.get('idthanhvien')
            thanhvien = ThanhVienLop.objects.get(idthanhvien = idthanhvien)

            thanhvien_seria = ThanhVienLopSerializer(thanhvien)
            idlophoc = thanhvien_seria.data.get('idlophoc')
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

            donnghi.trangthai = trangthai
            donnghi.thoigianphanhoi = thoigianphanhoi
            donnghi.save()

            donnghi_seria = DonXinNghiSerializer(donnghi)

            return Response(
                {
                    'code' : 1000,
                    'message': 'OK',
                    'Thong tin sau khi sua' : donnghi_seria.data
                }
                ,status= status.HTTP_202_ACCEPTED
            )
        
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

    #Get form list for teacher
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
            
            list_form = []
            user_id = user.id
            giangvien = GiangVien.objects.get(id = user_id)
            idgiangvien = giangvien.idgiangvien
            
            data = request.data
            idlophoc = data['idlophoc']
            if idlophoc or (not is_valid_param(idlophoc)):
                return Response(
                    {
                        'code' : 1004,
                        'message': 'Invaild id. Please check input again.' 
                    }
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return Response(
                    {
                        'code' : 1009,
                        'message': 'Class not found. Please try again.' 
                    }
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            
            lophoc  = LopHoc.objects.get(idlophoc = idlophoc)
            tenlophoc = lophoc.tenlophoc
            if lophoc.idgiangvien != idgiangvien:
                return Response(
                    {
                        'code' : 1009,
                        'message': 'This teacher doesnt manage this class and have necessary permission' 
                    }
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            
            thanhvienlop = ThanhVienLop.objects.filter(idlophoc = idlophoc)
            thanhvienlop_seria = ThanhVienLopSerializer(thanhvienlop, many = True)
            for group in thanhvienlop_seria.data :
                idsinhvien = group.get('idsinhvien')
                sinhvien = SinhVien.objects.get(idsinhvien = idsinhvien)
                tensinhvien = sinhvien.tensinhvien

                idthanhvien = group.get('idthanhvien')
                donnghi = DonXinNghi.objects.filter(idthanhvien = idthanhvien)
                donnghi_seria = DonXinNghiSerializer(donnghi, many = True)
                for group in donnghi_seria.data :
                    ngayxinnghi = group.get('ngayxinnghi')
                    lydo = group.get('lydo')
                    trangthai = group.get('trangthai')
                    thoigiangui = group.get('thoigiangui')

                    if trangthai != 0:
                        thoigianphanhoi = group.get('thoigianphanhoi')
                        list_form.append(
                            {
                                "Id sinh vien" : idsinhvien,
                                "Ten sinh vien" : tensinhvien,
                                "Ngay xin nghi" : ngayxinnghi,
                                "Ly do" : lydo,
                                "Trang thai" : trangthai,
                                "Thoi gian gui don" : thoigiangui,
                                "Thoi gian da phan hoi" : thoigianphanhoi
                            }
                        )
                    else:
                        list_form.append(
                            {
                                "Id sinh vien" : idsinhvien,
                                "Ten sinh vien" : tensinhvien,
                                "Ngay xin nghi" : ngayxinnghi,
                                "Ly do" : lydo,
                                "Trang thai" : trangthai,
                                "Thoi gian gui don" : thoigiangui,
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
                    'Danh sach yeu cau vang mat': list_form
                }, 
                status= status.HTTP_200_OK
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong!'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
