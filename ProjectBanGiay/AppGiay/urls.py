from django.urls import path
from . import views_server
from . import views_client

urlpatterns = [
    path("", views_server.home, name="home")
]