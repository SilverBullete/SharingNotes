from django.urls import path
from . import views

urlpatterns = [
    path('get_hottest', views.get_hottest),
    path("get_recommend", views.get_recommend),
    path("login/", views.get_user_info),
]