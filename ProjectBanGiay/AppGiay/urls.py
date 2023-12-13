from django.urls import path
from .views_server import ManageDanhMucGiay, ManageOrder, ManageKhachHangAccount, ManageChitietGiay
from .views_server import LoginView, ManageAccount
from .views_client import ManageGioHang, ManageReview, HistoryActivities, ShowDetailsAccount, GetDetailsGiay

urlpatterns = [
    #server
    path('manageDanhmucgiay', ManageDanhMucGiay.as_view()),
    path('manageChitietgiay', ManageChitietGiay.as_view()),
    path('manageAccount', ManageAccount.as_view()),
    path('manageOrder', ManageOrder.as_view()),
    path('login', LoginView.as_view()),

    #Client
    path('detailsGiay', GetDetailsGiay.as_view()),
    path('giohangKhachhang', ManageGioHang.as_view()),
    # path('review', ManageReview.as_view()),
    # path('lichsuMuahang', HistoryActivities.as_view()),
    # path('detailsAccount', ShowDetailsAccount.as_view()),
    # path('manageGuestaccount', ManageKhachHangAccount.as_view()),

]