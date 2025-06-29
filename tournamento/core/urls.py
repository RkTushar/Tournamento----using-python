from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tournament/<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
    path('tournament/<int:tournament_id>/edit/', views.edit_tournament, name='edit_tournament'),
    path('tournament/<int:tournament_id>/delete/', views.delete_tournament, name='delete_tournament'),
]
