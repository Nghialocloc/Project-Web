from django.urls import path
from .views_server import ManageDanhMucGiay, ManageOrder, ManageAccount, ManageKhachHangAccount, DetailListDanhmuc
from .views_client import ManageGioHang, ManageReview, HistoryActivities, ShowDetailsAccount, GetDetailsGiay
from . import views_server

urlpatterns = [
    path("", views_server.home, name="home"),
    path('manageDanhmucgiay', ManageDanhMucGiay.as_view()),
    path('manageAccount', ManageAccount.as_view()),
    path('manageGuestaccount', ManageKhachHangAccount.as_view()),
    path('manageOrder', ManageOrder.as_view()),
    path('thongkeGiay', DetailListDanhmuc.as_view()),
    path('giohangKhachhang', ManageGioHang.as_view()),
    path('review', ManageReview.as_view()),
    path('lichsuMuahang', HistoryActivities.as_view()),
    path('detailsAccount', ShowDetailsAccount.as_view()),
    path('detailsGiay', GetDetailsGiay.as_view())

]