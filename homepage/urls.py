from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('mypage/', views.mypage),
    path('company/', views.company)

]