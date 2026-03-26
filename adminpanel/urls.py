from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),

    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
     path('login/', views.admin_login, name='admin_login'),
]