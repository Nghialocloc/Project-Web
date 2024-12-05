from rest_framework import generics, permissions, status, authentication
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SinhVien, GiangVien
from .models import UserAccount, UserAccountManager
from .serializers import UserAccountSerializer
from .serializers import SinhVienSerializer, GiangVienSerializer
from django.contrib.auth import get_user_model
import traceback
import random, string
import datetime
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# Create your views here.
def is_valid_param(param) :
    return param != " " and param is not None and param != ""


def id_generator (size, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Class quan li he thong nguoi dung
def insert_sinhvien(requested_data,Email,accountName,user):

    namhoc = requested_data['namhoc']
    while True:
        sinhvien = id_generator(size=4)
        idsinhvien = str(namhoc) + str(sinhvien)
        if (SinhVien.objects.filter(idsinhvien=  int(idsinhvien) ).count() == 0):
            break
    tensinhvien = requested_data['tensinhvien']
    nganhhoc = requested_data['nganhhoc']
    diachi = requested_data['diachi']
    sdt = requested_data['sdt']
    user_id = user
    
    student = SinhVien(idsinhvien=idsinhvien,tensinhvien=tensinhvien, nganhhoc=nganhhoc,
                        diachi=diachi,sdt=sdt,id = user_id)
    student.save()
    
    return student

def insert_giangvien(requested_data,Email,accountName,user):
    while True:
        giangvien = id_generator(size=8)
        if (GiangVien.objects.filter(idgiangvien=giangvien).count() == 0):
            break
    tengiangvien = requested_data['tengiangvien']
    tenchucvu = requested_data['tenchucvu']
    diachi = requested_data['diachi']
    sdt = requested_data['sdt']
    user_id = user
    
    teacher = GiangVien(idgiangvien=giangvien,tengiangvien=tengiangvien, tenchucvu=tenchucvu
                        , diachi=diachi, sdt=sdt, id = user_id)
    teacher.save()
    
    return teacher


class ManageAccount(APIView):
    permission_classes = (permissions.AllowAny, )
    
    #Create user info
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
            is_teacher = data['is_teacher']
            
            if password ==  re_password:
                if len(password) >= 8:
                    if not UserAccount.objects.filter(email=email).exists():
                        if not is_teacher:
                            student = User.objects.create_student(email = email, accountname=accountname, sex = gioitinh, 
                                                                  brithday = ngaysinh, joined = date_joined, password=password)
                            insert_sinhvien(requested_data=data,Email=email,accountName=accountname,user=student)
                            return Response(
                                {"success": "User successfully created"},
                                status= status.HTTP_201_CREATED
                            )
                        else: 
                            teacher = User.objects.create_teacher(email = email, accountname=accountname, sex = gioitinh, 
                                                                  brithday = ngaysinh, joined = date_joined, password=password)
                            insert_giangvien(requested_data=data,Email=email,accountName=accountname,user=teacher)
                            return Response(
                                {"success": "User successfully created"},
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

    #Get all user info
    def get(self, request):
        try:
            user= request.user
            if ( not user.is_teacher ) or user.is_active == False:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
            )

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

    #Set user info
    def put(self, request):
        try: 
            user= request.user
            if ( not user.is_teacher ) or user.is_active == False:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
            )

            else:
                number = request.data['id']
                accountname = request.data['accountname']
                gioitinh = request.data['gioitinh']
                ngaysinh = request.data['ngaysinh']
                
                account = UserAccount.objects.get(id=number)
                account.accountname = accountname
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


class ManageSingleUser(APIView):

    permission_classes = (permissions.AllowAny, )

    #Get single user info
    def get(self, request, format=None):
        try:
            user = request.user
            user_seria = UserAccountSerializer(user)
            user_id = user.id
            
            if not user.is_teacher:
                user_detail = SinhVien.objects.get(id = user_id) 
                detail = SinhVienSerializer(user_detail)
            else:
                user_detail = GiangVien.objects.get(id = user_id)
                detail = GiangVienSerializer(user_detail)

            return Response(
                {
                    'user': user_seria.data,
                    'detail': detail.data
                 },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class ChangeAccountState(APIView):

    permission_classes = (permissions.AllowAny, )

    #Activate or deactive user
    def put(self, request):
        try: 
            user= request.user
            if ( not user.is_teacher ) or user.is_active == False:
                return Response(
                    {'error': 'User does not have necessary permission' }, 
                    status=status.HTTP_403_FORBIDDEN
            )

            number = request.data['id']
            option = request.data['option']
            if User.objects.filter(id = number).count() == 0:
                return  Response(
                    {'error': 'Khong tim thay user'}, 
                    status= status.HTTP_404_NOT_FOUND
                )

            account = UserAccount.objects.get(id=number)
            
            if(option == 0):
                account.is_active = False
                account.save()
                return Response(
                    {'Update success. Deactivate user'}, 
                    status= status.HTTP_202_ACCEPTED
                )
            elif (option == 1) :
                account.is_active = True
                account.save()
                return Response(
                    {'Update success. Activate user'}, 
                    status= status.HTTP_202_ACCEPTED
                )
            else :
                return Response(
                    {'error': 'Index out of bound'}, 
                    status= status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

from ProjectBanGiay.view import MyTokenObtainPairSerializer, MyTokenObtainPairView

class LoginView(MyTokenObtainPairView):
    permission_classes = (permissions.AllowAny, )

    #Login
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return response
        except Exception as e:
            return Response({
            'error': True,
            'message': 'Invalid Username or Password',
        }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):

    permission_classes = (permissions.AllowAny, )

     #Logout
    def post(self, request):
        try:
            user = request.user
            user_seria = UserAccountSerializer(user)
            if(user_seria.is_valid):
                re_token = RefreshToken(request.data.get('refresh'))
                re_token.blacklist()
                return Response(
                    {"Message" : "User has been logout"}, 
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"Message" : "User not found or not vaild"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )