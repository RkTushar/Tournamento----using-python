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

    # Round-robin match generation
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

    # Only setup if not already done
    if tournament.teams.exists():
        return redirect('home')

    # Create Groups
    groups = []
    for i in range(tournament.total_groups):
        group_name = chr(65 + i)  # A, B, C...
        group = Group.objects.create(name=f"Group {group_name}", tournament=tournament)
        groups.append(group)

    # Create Teams
    teams = []
    for i in range(tournament.total_teams):
        team = Team.objects.create(name=f"Team {i+1}", tournament=tournament)
        teams.append(team)

    # Shuffle and assign teams to groups
    random.shuffle(teams)
    for i, team in enumerate(teams):
        group = groups[i % tournament.total_groups]
        team.group = group
        team.save()

    # Generate fixtures
    for group in tournament.groups.all():
        generate_group_fixtures(group)

    return redirect('home')
