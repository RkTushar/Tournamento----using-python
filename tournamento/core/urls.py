from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tournament/<int:tournament_id>/setup/', views.setup_tournament, name='setup_tournament'),
    path('tournament/<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
    path('match/<int:match_id>/update/', views.update_match_score, name='update_match_score'),
]
