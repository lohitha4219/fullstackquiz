from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),

    path('home/', views.quiz_home, name='dashboard'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # 🔥 IMPORTANT: keep specific URLs FIRST
    path("start/<str:domain>/<str:level>/", views.start_quiz, name="start_quiz"),
    path("submit/", views.submit_answer, name="submit_answer"),
    path("quit/", views.quit_quiz, name="quit_quiz"),
    path("result/", views.quiz_result, name="quiz_result"),

    path("download-result/", views.download_result, name="download_result"),
    path("download-certificate/", views.download_certificate, name="download_certificate"),

    # 🔥 KEEP THIS LAST ALWAYS
    path("<str:domain>/", views.choose_level, name="choose_level"),

    
]