from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as acc_views
from quiz import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('dashboard/', acc_views.dashboard, name='dashboard'),
    path('logout/', acc_views.logout_view, name='logout'),
    path('edit-profile/', acc_views.edit_profile, name='edit_profile'),
    path('quiz/', include('quiz.urls')),
    path('leaderboard/', include('leaderboard.urls')),
    path('', views.login_view, name='login'),   # 👈 main login
    path('dashboard/', acc_views.dashboard, name='dashboard')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)