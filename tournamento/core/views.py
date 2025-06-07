from django.shortcuts import get_object_or_404, redirect, render
from .models import Tournament
from .utils import assign_groups_and_generate_fixtures

def setup_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    assign_groups_and_generate_fixtures(tournament)
    return redirect('tournament_detail', tournament_id=tournament.id)
