from django.urls import path
from .QuanLyTK import ManageAccount, ManageSingleUser, ChangeAccountState
from .QuanLyLopHoc import ManageClassTeacher, ManageClassMember, ManageClassStudent


urlpatterns = [
    #QuanLyTK
    path('AdminManageAccount', ManageAccount.as_view()),
    path('ManageAccount', ManageSingleUser.as_view()),
    path('AccountActivation', ChangeAccountState.as_view()),

    #QuanLyLopHoc
    path('AdminManageClass', ManageClassTeacher.as_view()),
    path('ManageClass', ManageClassMember.as_view()),
    path('InfoClass', ManageClassStudent.as_view()),

    #QuanLyDonNghi
]