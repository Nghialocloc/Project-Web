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

User = get_user_model()

def get_member_id(sinhvien, lophoc):
    thanhvien = ThanhVienLop.objects.get(idsinhvien = sinhvien, idlophoc = lophoc)
    return thanhvien.idthanhvien

# Create your views here.
def is_valid_param(param) :
    return param != " " and param is not None and param != ""


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
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            sinhvien = SinhVien.objects.get(id = user.id)
            idsinhvien = sinhvien.idsinhvien
            idlophoc = data['idlophoc']
            if LopHoc.objects.filter(idlophoc = idlophoc).count() == 0:
                return  Response(
                    {'error': 'Loi du lieu. Khong tim thay thong tin lop.'}, 
                    status= status.HTTP_404_NOT_FOUND
                )
            
            else: 
                while True:
                    iddon = id_generator(size=10)
                    if (DonXinNghi.objects.filter(iddon = iddon).count() == 0):
                        break                      
                
                idthanhvien = get_member_id(idsinhvien, idlophoc)
                ngayxinnghi = data['ngayxinnghi']
                lydo = data['lydo']
                trangthai = 0
                thoigiangui = datetime.datetime.now()

                hientai = datetime.date.today()

                if ngayxinnghi < hientai:
                    return Response(
                        {"Thong tin ngay da qua han. Vui long nhap lai"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                donnghi = DonXinNghi(iddon = iddon, idthanhvien = idthanhvien, ngayxinnghi = ngayxinnghi, lydo = lydo,
                                     trangthai = trangthai, thoigiangui = thoigiangui)
                donnghi.save()
                
                return Response(
                    {"Da gui don len he thong"},
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
            if (not user.is_teacher) or user.is_active == False:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            data=request.data
            iddon = data['iddon']
            if DonXinNghi.objects.filter(iddon = iddon).count() == 0:
                return Response(
                    {'error': 'No matching data'}
                    ,status= status.HTTP_404_NOT_FOUND
                )
            
            trangthai = data['trangthai']
            thoigianphanhoi = datetime.datetime.now()
            donnghi = DonXinNghi.objects.get(iddon = iddon)
            donnghi.trangthai = trangthai
            donnghi.thoigianphanhoi = thoigianphanhoi
            donnghi.save()

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
        

    #Get form list for teacher
    def get(self, request):
        try:
            user = request.user
            if (not user.is_teacher):
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            list_form = []
            user_id = user.id
            giangvien = GiangVien.objects.get(id = user_id)
            idgiangvien = giangvien.idgiangvien
            
            data = request.data
            idlophoc = data['idlophoc']
            if LopHoc.objects.filter(idgiangvien = idgiangvien, idlophoc = idlophoc).count() == 0:
                return Response(
                    {'error': 'No matching data. Lop khong ton tai hoac khong thuoc quyen cua giang vien'}
                    ,status= status.HTTP_400_BAD_REQUEST
                )
            lophoc  = LopHoc.objects.get(idgiangvien = idgiangvien, idlophoc = idlophoc)
            tenlophoc = lophoc.tenlophoc
            
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
