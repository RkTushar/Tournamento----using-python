from django.shortcuts import render, redirect, get_object_or_404
from .models import Tournament, Team, Group
import random

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        total_teams = int(request.POST.get('total_teams'))
        total_groups = int(request.POST.get('total_groups'))

        Tournament.objects.create(
            name=name,
            total_teams=total_teams,
            total_groups=total_groups
        )
        return redirect('home')

    tournaments = Tournament.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'tournaments': tournaments})


def setup_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.method == 'POST':
        team_names = request.POST.getlist('team_names')

        # Optional: Clear old data
        Team.objects.filter(tournament=tournament).delete()
        Group.objects.filter(tournament=tournament).delete()

        # Create groups
        groups = []
        for i in range(tournament.total_groups):
            group = Group.objects.create(
                name=chr(65 + i),  # A, B, C, ...
                tournament=tournament
            )
            groups.append(group)

        # Shuffle and assign teams
        random.shuffle(team_names)
        for i, name in enumerate(team_names):
            group = groups[i % tournament.total_groups]
            Team.objects.create(name=name, group=group, tournament=tournament)

        return redirect('home')  # You can change this to a group/match page later

    return render(request, 'core/setup_tournament.html', {
        'tournament': tournament,
        'team_count': range(tournament.total_teams)
    })
