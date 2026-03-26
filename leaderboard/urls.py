from django.urls import path
from .views import leaderboard

urlpatterns = [
    path("", leaderboard, name="leaderboard"),
    path("<str:domain>/", leaderboard, name="leaderboard_domain"),
]