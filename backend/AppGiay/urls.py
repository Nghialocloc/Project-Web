from django.urls import path
from .QuanLyTK import ManageAccount, ManageSingleUser


urlpatterns = [
    #Server
    path('AdminManageAccount', ManageAccount.as_view()),
    path('ManageAccount', ManageSingleUser.as_view()),

]