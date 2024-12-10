from rest_framework import generics, permissions, status
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
from rest_framework_simplejwt.authentication import JWTAuthentication
JWT_authenticator = JWTAuthentication()

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
                if len(password) < 6 or len(password) > 12:
                    if not UserAccount.objects.filter(email=email).exists():
                        if not is_teacher:
                            student = User.objects.create_student(email = email, accountname=accountname, sex = gioitinh, 
                                                                  brithday = ngaysinh, joined = date_joined, password=password)
                            insert_sinhvien(requested_data=data,Email=email,accountName=accountname,user=student)
                            return Response(
                                {
                                    'code': "1000",
                                    'message' : "OK"
                                },
                                status= status.HTTP_201_CREATED
                            )
                        else: 
                            teacher = User.objects.create_teacher(email = email, accountname=accountname, sex = gioitinh, 
                                                                  brithday = ngaysinh, joined = date_joined, password=password)
                            insert_giangvien(requested_data=data,Email=email,accountName=accountname,user=teacher)
                            return Response(
                                {
                                    'code': "1000",
                                    'message' : "OK"
                                },
                                status= status.HTTP_201_CREATED
                            )
                    else:
                        return Response(
                            {
                                'code': "9996",
                                'message' : "User has already exsit"
                            },
                            status= status.HTTP_400_BAD_REQUEST
                            )
                else:
                    return Response(
                        {
                            'code' : "1004",
                            'messsage': "Password must have more than 6 character and less than 10 character"
                        },
                        status= status.HTTP_400_BAD_REQUEST
                        )
                    
            else:
                return Response(
                    {
                        'code' : "1004",
                        'messsage': 'Password do not match'
                    },
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
            if ( not user.is_teacher ):
                return Response(
                    {
                        'code' : "1009",
                        'message': 'User does not have necessary permission' 
                    }, 
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
            if ( not user.is_teacher ):
                return Response(
                    {
                        'code' : "1009",
                        'message': 'User does not have necessary permission' 
                    },
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


class ChangeInfo(APIView):

    permission_classes = (permissions.AllowAny, )

    #Get single user info
    def get(self, request, format=None):
        try:
            data = request.data

            option = data['option']

            if option == 0:
                user_id = data["user_id"]
                if is_valid_param(user_id) == False or UserAccount.objects.filter(id = user_id).count() == 0:
                    return Response(
                        {
                            'code' : 9995,
                            'message' : "User not found. Please check input again", 
                        }, 
                        status=status.HTTP_403_FORBIDDEN
                )

                user = UserAccount.objects.get(id = user_id)

                if not user.is_teacher:
                    user_detail = SinhVien.objects.get(id = user_id) 
                    detail = SinhVienSerializer(user_detail)
                else:
                    user_detail = GiangVien.objects.get(id = user_id)
                    detail = GiangVienSerializer(user_detail)

                return Response(
                    {
                        'code' : 1000,
                        'message' : "OK",
                        'user': 
                        {
                            "username" : user.accountname,
                            "email" : user.email
                        }
                        ,'detail': detail.data
                    },
                    status=status.HTTP_200_OK
                )
            elif option == 1:
                user = request.user
                user_id = user.id

                if not user.is_teacher:
                    user_detail = SinhVien.objects.get(id = user_id) 
                    detail = SinhVienSerializer(user_detail)
                else:
                    user_detail = GiangVien.objects.get(id = user_id)
                    detail = GiangVienSerializer(user_detail)

                return Response(
                    {
                        'code' : 1000,
                        'message' : "OK",
                        'user': 
                        {
                            "username" : user.accountname,
                            "email" : user.email
                        }
                        ,'detail': detail.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'code' : 1004,
                        'message' : "Out of bound. Please check input data option value",
                    },
                    status=status.HTTP_400_BAD_REQUEST
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
            if ( not user.is_teacher ):
                return Response(
                    {
                        'code' : 1009,
                        'message': 'User does not have necessary permission' 
                    },
                    status=status.HTTP_403_FORBIDDEN
            )

            number = request.data['id']
            option = request.data['option']
            if User.objects.filter(id = number).count() == 0:
                return  Response(
                    {
                        'code' : 9995,
                        'message' : "User not found",
                    }, 
                    status= status.HTTP_404_NOT_FOUND
                )

            account = UserAccount.objects.get(id=number)
            
            if(option == 0):
                account.is_active = False
                account.save()
                return Response(
                    {
                        'code' : 1000,
                        'message' : 'Update success. Deactivate user'
                    }, 
                    status= status.HTTP_202_ACCEPTED
                )
            elif (option == 1) :
                account.is_active = True
                account.save()
                return Response(
                    {
                        'code' : 1000,
                        'message' : 'Update success. Activate user'
                    },  
                    status= status.HTTP_202_ACCEPTED
                )
            else :
                return Response(
                    {
                        'code' : 1004,
                        'message' : "Out of bound. Please check input data option value",
                    },
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
            email = request.data['email']
            password = request.data['password']
            if is_valid_param(email) == False or is_valid_param(password) == False:
                return Response(
                    {
                        'code': 1004,
                        'message': 'Parameter is null',
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            if UserAccount.objects.filter(email = email). count() == 0:
                return Response(
                    {
                        'code': 9995,
                        'message': 'User not found',
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            response = super().post(request, *args, **kwargs)
            return response

        except Exception as e:
            return Response(
                {
                    'code': 1004,
                    'message': 'Invalid Password',
                },
                status=status.HTTP_401_UNAUTHORIZED
                )


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
                    {
                        "code" : 1000,
                        "message" : "User has been logout"
                    }, 
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "code" : 9995,
                        "message" : "User not found or not vaild"
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyToken(APIView):
    permission_classes = (permissions.AllowAny, )

     #Verify
    def post(self, request):
        try:
            jwt_object  = JWT_authenticator
            header          = jwt_object.get_header(request)
            raw_token       = jwt_object.get_raw_token(header)
            validated_token = jwt_object.get_validated_token(raw_token)
            user  = jwt_object.get_user(validated_token)


            return Response(
                {
                    'code': 1000,
                    'message' : "OK",
                    'data' : 
                    {
                        "id" : user.id,
                        "token" : validated_token.payload,
                        "active" : user.is_active
                    }
                }
            )
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Something went wrong'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )