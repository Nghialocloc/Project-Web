from django.urls import path
from .QuanLyTK import ManageAccount, ManageSingleUser, ChangeAccountState, LogoutView, LoginView
from .QuanLyLopHoc import ManageClassTeacher, ManageClassMember, ManageClassStudent
from .QuanLyDonNghi import ManageAbsenceForm


urlpatterns = [
    #QuanLyTK
    path('AdminManageAccount', ManageAccount.as_view()),
    path('AccountInfo', ManageSingleUser.as_view()),
    path('AccountActivation', ChangeAccountState.as_view()),
    path('Login', LoginView.as_view()),
    path('Logout', LogoutView.as_view()),

    #QuanLyLopHoc
    path('AdminManageClass', ManageClassTeacher.as_view()),
    path('ManageClass', ManageClassMember.as_view()),
    path('ClassInfo', ManageClassStudent.as_view()),

    #QuanLyDonNghi
    path('ManageAbsence', ManageAbsenceForm.as_view()),
]