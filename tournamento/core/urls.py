from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tournament/<int:tournament_id>/setup/', views.setup_tournament, name='setup_tournament'),
]
