from django.urls import path
from .views_server import DanhMucGiayManage, OrderList
from .views_server import CreateAccount, RetrieveAccountView, UpdateAccountView, DeleteAccount
from .views_client import ManageGioHang
from . import views_server

urlpatterns = [
    path("", views_server.home, name="home"),
    path('danhmucgiay', DanhMucGiayManage.as_view()),
    path('order_list', OrderList.as_view()),
    path('create_account', CreateAccount.as_view()),
    path('retrieve_account', RetrieveAccountView.as_view()),
    path('update_account', UpdateAccountView.as_view()),
    path('delete_account', DeleteAccount.as_view()),
    path('giohang_khachhang', ManageGioHang.as_view())

]