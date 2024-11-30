from django.urls import path
from .QuanLyTK import ManageAccount, ManageSingleUser, ChangeAccountState


urlpatterns = [
    #QuanLyTK
    path('AdminManageAccount', ManageAccount.as_view()),
    path('ManageAccount', ManageSingleUser.as_view()),
    path('AccountActivation', ChangeAccountState.as_view()),

    
]