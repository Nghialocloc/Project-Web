from django.shortcuts import HttpResponse
from django.http import JsonResponse
from pymysql import NULL
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserAccount, UserAccountManager
from .serializers import UserAccountSerializer
from django.contrib.auth import get_user_model
import traceback
import random, string
import datetime

User = get_user_model()

def is_valid_param(param) :
    return param != '' and param is not None and param != ""

def id_generator (size = 5, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

