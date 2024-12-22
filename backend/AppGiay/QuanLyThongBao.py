from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import UserAccount
from .serializers import UserAccountSerializer
from .models import ThongbBaoTinNhan
from .serializers import ThongbBaoTinNhanSerializer
import traceback
import requests
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
import random, string
import datetime

User = get_user_model()

def is_valid_param(param) :
    return (param != " ") and (param is not None) and (param != "")


def id_generator (size, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_random_string(length):
    chars = string.ascii_letters + string.digits
    rand_chars = ''.join(random.choices(chars,k=length))
    return rand_chars


# Create your views here.
class MessageSender(APIView):

    serializer_class = ThongbBaoTinNhanSerializer

    permission_classes = (permissions.AllowAny, )

    def post(self,request):
        try:
            data = request.data
            user = request.user
            # Thay thế với thông tin user trong authorization
            sender_id  = user.id

            # Block này cứ tiếp tục như thường
            receiver_id = data['user_id']

            if not is_valid_param(receiver_id):
                return Response(
                        {
                            'code' : 1002,
                            'message' : "Missing user id. Please add mising input", 
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            if UserAccount.objects.filter( id = receiver_id).count() == 0:
                return Response(
                        {
                            'code' : 9995,
                            'message' : "User not found. Please check input again", 
                        }, 
                        status=status.HTTP_404_NOT_FOUND
                    )

            message = data['message']
            if not is_valid_param(message):
                return Response(
                        {
                            'code' : 1002,
                            'message' : "Missing message detail. Please add mising input", 
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            if len(message) > 200:
                return Response(
                        {
                            'code' : 1004,
                            'message' : "Message detail is long than 200 character. Please change input", 
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            type = data['type']
            if not is_valid_param(message):
                return Response(
                        {
                            'code' : 1002,
                            'message' : "Missing type of message. Please add mising input", 
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            related_id = data['related_id']
            is_read = False

            while True:
                message_id = generate_random_string(length=8)
                if (ThongbBaoTinNhan.objects.filter(message_id = message_id).count() == 0):
                    break

           
            msgstr = ThongbBaoTinNhan(message_id = message_id, sender_id = sender_id, receiver_id = receiver_id, message = message,
                                      type = type, related_id = related_id, is_read = is_read)
            msgstr.save()

            return Response(
                {
                    'code':1000, 
                    'message':"OK"
                }, 
                status=status.HTTP_201_CREATED
            )    
                    
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}, 
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    
    #Get list nofitcation
    def get(self, request):
        try:
            data = request.data
            user = request.user
            # Thay thế với thông tin user trong authorization
            receiver_id  = user.id

            if ThongbBaoTinNhan.objects.filter(receiver_id = receiver_id).count() == 0:
                return Response(
                        {
                            'code' : 1000,
                            'message' : "User account have received no message", 
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            index = int(data['index'])
            if ThongbBaoTinNhan.objects.filter(receiver_id = receiver_id) < index or (not is_valid_param(index)):
                return Response(
                        {
                            'code' : 1002,
                            'message' : "Invalid index input. Please check input again", 
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            count = int(data['count'])
            if ThongbBaoTinNhan.objects.filter(receiver_id = receiver_id) < (index + count):
                return Response(
                        {
                            'code' : 1004,
                            'message' : "The number of request message is too big. Please change the number", 
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            received_notifs = ThongbBaoTinNhan.objects.filter(receiver_id = receiver_id)[index:index + count]
            received_notifs = ThongbBaoTinNhanSerializer(received_notifs, many = True)    
            return Response(
                {
                    'code':1000,
                    'message':'OK',
                    'Danh sach thong bao duoc gui toi': received_notifs.data
                }
            ) 
        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}
                , status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #mark nofication as read
    def put(self, request):
        try:
            data = request.data
            user = request.user
            read_list = []

            # Thay thế với thông tin user trong authorization
            receiver_id  = user.id
            if ThongbBaoTinNhan.objects.filter(receiver_id = receiver_id).count() == 0:
                return Response(
                        {
                            'code' : 1000,
                            'message' : "User account have received no message", 
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            notification_list = data['notification_list']
            received_notifs = ThongbBaoTinNhan.objects.filter(receiver_id = receiver_id)
            received_notifs_seria = ThongbBaoTinNhanSerializer(received_notifs, many = True)
            for group in received_notifs_seria:
                message_id = group.get('message_id')
                if message_id in notification_list:
                    message = ThongbBaoTinNhan.objects.get(message_id = message_id)
                    if message.is_read == False:
                        message.is_read = True

                    read = ThongbBaoTinNhanSerializer(message)
                    read_list.append(read)

            return Response(
                {
                    'code':1000,
                    'message':'OK',
                    'Danh sach thong bao duoc doc': read_list
                }
            ) 

        except Exception as e:
            traceback.print_exc()
            return Response(
                {'error': 'Some exeption happened'}
                , status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )
