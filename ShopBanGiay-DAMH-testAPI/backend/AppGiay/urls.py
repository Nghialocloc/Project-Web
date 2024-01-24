from django.urls import path
from .views_server import DanhMucGiayManage, ManageAccount, KhachHangAccountManager
from .views_client import ManageGioHang, ReviewManager, KhachHangAccountActivities
from . import views_server

urlpatterns = [
    path("", views_server.home, name="home"),
    path('manageDanhmucgiay', DanhMucGiayManage.as_view()),
    path('manageAccount', ManageAccount.as_view()),
    path('manageguestaccount', KhachHangAccountManager.as_view()),
    path('giohangKhachhang', ManageGioHang.as_view()),

]