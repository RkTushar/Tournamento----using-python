from django.shortcuts import render, get_object_or_404, redirect
from .models import Tournament

def home(request):
    tournaments = Tournament.objects.all()
    return render(request, 'core/home.html', {'tournaments': tournaments})

def setup_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.method == 'POST':
        # You'll process group/team setup here later
        return redirect('setup_tournament', tournament_id=tournament.id)

    return render(request, 'core/setup_tournament.html', {'tournament': tournament})
