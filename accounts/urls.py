from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_register, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),  # 🔥 This fixes error
    path("register/", views.login_register, name="register"),
    path("logout/", views.logout_view, name="logout"),
]