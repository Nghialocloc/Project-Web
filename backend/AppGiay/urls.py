from django.urls import path
from .QuanLyTK import ManageAccount, ChangeInfo, ChangeAccountState, LogoutView, LoginView, VerifyToken
from .QuanLyLopHoc import ManageClassTeacher, ManageClassStudent, GetClassInfo
from .QuanLyDonNghi import ManageAbsenceForm
from .QuanLyDiemDanh import ManageAttendanceClass, GetAttendanceRecord
from .QuanLyTaiLieu import ManageMaterial, GetMaterialInfo


urlpatterns = [
    #QuanLyTK
    path('AdminManageAccount', ManageAccount.as_view()),
    path('AccountInfo', ChangeInfo.as_view()),
    path('AccountActivation', ChangeAccountState.as_view()),
    path('Login', LoginView.as_view()),
    path('Logout', LogoutView.as_view()),
    path('Verify', VerifyToken.as_view()),

    #QuanLyLopHoc
    path('AdminManageClass', ManageClassTeacher.as_view()),
    path('ManageClass', ManageClassStudent.as_view()),
    path('ClassInfo', GetClassInfo.as_view()),

    #QuanLyDonNghi
    path('ManageAbsence', ManageAbsenceForm.as_view()),

    #QuanLyDiemDanh
    path('ManageAttendance', ManageAttendanceClass.as_view()),
    path('AttendanceInfo', GetAttendanceRecord.as_view()),

    #QuanLyTaiLieu
    path('ManageMaterial', ManageMaterial.as_view()),
    path('MaterialInfo', GetMaterialInfo.as_view()),

]