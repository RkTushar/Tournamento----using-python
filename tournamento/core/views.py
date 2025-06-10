from django.shortcuts import render, redirect, get_object_or_404
from .models import Tournament, Team, Group, Match
import random
import itertools

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

def generate_group_fixtures(group):
    teams = list(group.teams.all())
    matches = []

    # Round-robin match generation: each pair plays one match
    for team_a, team_b in itertools.combinations(teams, 2):
        match = Match.objects.create(
            group=group,
            team_a=team_a,
            team_b=team_b,
        )
        matches.append(match)

    return matches

def setup_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    team_count = range(tournament.total_teams)

    if request.method == 'POST':
        team_names = request.POST.getlist('team_names')

        # Clear existing groups, teams, and matches for a clean slate
        tournament.matches.all().delete()
        tournament.groups.all().delete()
        tournament.teams.all().delete()

        # Create groups named A, B, C, ...
        groups = []
        for i in range(tournament.total_groups):
            group_name = chr(ord('A') + i)
            group = Group.objects.create(name=f"Group {group_name}", tournament=tournament)
            groups.append(group)

        # Create teams with names from user input, assign evenly to groups
        for idx, name in enumerate(team_names):
            group = groups[idx % tournament.total_groups]
            Team.objects.create(name=name, tournament=tournament, group=group)

        # Generate fixtures for each group
        for group in groups:
            generate_group_fixtures(group)

        return redirect('home')

    # GET request: render form to input team names
    return render(request, 'core/setup_tournament.html', {
        'tournament': tournament,
        'team_count': team_count,
    })
