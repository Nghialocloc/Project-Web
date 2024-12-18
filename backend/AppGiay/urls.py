from django.urls import path
from .QuanLyTK import ManageAccount, ChangeInfo, ChangeAccountState, LogoutView, LoginView, VerifyToken
from .QuanLyLopHoc import ManageClass, ManageClassStudent, GetClassInfo, ManageStudent
from .QuanLyDonNghi import ManageAbsenceForm
from .QuanLyDiemDanh import ManageAttendanceClass, GetAttendanceRecord
from .QuanLyTaiLieu import ManageMaterial, GetMaterialInfo
from .QuanLyBaiTap import ManageAssignment, SubmitHomework, ManageHomework, GetAssignmemntInfo, GetAssignmemntList


urlpatterns = [
    #QuanLyTK
    path('AdminManageAccount', ManageAccount.as_view()),
    path('AccountInfo', ChangeInfo.as_view()),
    path('AccountActivation', ChangeAccountState.as_view()),
    path('Login', LoginView.as_view()),
    path('Logout', LogoutView.as_view()),
    path('Verify', VerifyToken.as_view()),

    #QuanLyLopHoc
    path('ManageClass', ManageClass.as_view()),
    path('ManageClassStudent', ManageClassStudent.as_view()),
    path('ManageStudent', ManageStudent.as_view()),
    path('ClassInfo', GetClassInfo.as_view()),

    #QuanLyDonNghi
    path('ManageAbsence', ManageAbsenceForm.as_view()),

    #QuanLyDiemDanh
    path('ManageAttendance', ManageAttendanceClass.as_view()),
    path('AttendanceInfo', GetAttendanceRecord.as_view()),

    #QuanLyTaiLieu
    path('ManageMaterial', ManageMaterial.as_view()),
    path('MaterialInfo', GetMaterialInfo.as_view()),

    #QuanLyBaiTap
    path('ManageAssignment', ManageAssignment.as_view()),
    path('ManageHomework', ManageHomework.as_view()),
    path('SummitHomework', SubmitHomework.as_view()),
    path('GetAssignmemntList', GetAssignmemntList.as_view()),
    path('GetAssignmemntInfo', GetAssignmemntInfo.as_view()),
]