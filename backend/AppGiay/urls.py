from django.urls import path
from .QuanLyTK import ManageAccount, ManageSingleUser


urlpatterns = [
    #Server
    path('Manage Account', ManageAccount.as_view()),
    path('Search Account', ManageSingleUser.as_view()),

]