from django.shortcuts import render, redirect, get_object_or_404
from .models import Tournament
from .forms import TournamentForm

def home(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournaments/home.html', {'tournaments': tournaments})

def setup_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.method == 'POST':
        # handle setup logic later (grouping, points system, etc.)
        pass

    return render(request, 'tournaments/setup.html', {'tournament': tournament})
