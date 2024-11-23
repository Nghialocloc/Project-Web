from django.urls import path
from .QuanLyTK import ManageAccount, RetriveSingleUser


urlpatterns = [
    #Server
    path('Manage Account', ManageAccount.as_view()),
    path('Search Account', RetriveSingleUser.as_view()),

]