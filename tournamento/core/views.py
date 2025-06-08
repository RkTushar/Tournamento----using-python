from django.shortcuts import render, get_object_or_404, redirect
from .models import Tournament

def home(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournamento/home.html', {'tournaments': tournaments})

def setup_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.method == 'POST':
        # Placeholder: Handle form logic later (group creation, etc.)
        return redirect('tournament_detail', tournament_id=tournament.id)

    return render(request, 'tournamento/setup_tournament.html', {'tournament': tournament})
