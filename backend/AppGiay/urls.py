from django.urls import path
from .views_server import ManageDanhMucGiay, ManageOrder, ManageChitietGiay
from .views_server import RetriveUserView, ManageAccount
from .views_client import ManageGioHang, GetDetailsGiay, GetReviewGiay
from .views_client import ManageReview, HistoryActivities, ShowDetailsAccount

urlpatterns = [
    #server
    path('manageDanhmucgiay', ManageDanhMucGiay.as_view()),
    path('manageChitietgiay', ManageChitietGiay.as_view()),
    path('manageAccount', ManageAccount.as_view()),
    path('manageOrder', ManageOrder.as_view()),
    path('retrive', RetriveUserView.as_view()),

    #Client
    path('detailsGiay', GetDetailsGiay.as_view()),
    path('reviewGiay', GetReviewGiay.as_view()),
    path('giohangKhachhang', ManageGioHang.as_view()),

    path('review', ManageReview.as_view()),
    path('lichsuMuahang', HistoryActivities.as_view()),
    path('detailsAccount', ShowDetailsAccount.as_view()),

]