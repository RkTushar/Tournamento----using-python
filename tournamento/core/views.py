from django.shortcuts import render, redirect, get_object_or_404
from .models import Tournament, Team, Group, Match
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
    return render(request, 'core/home.html', {
        'tournaments': tournaments
    })


def generate_group_fixtures(group):
    teams = list(group.teams.all())
    matches = []
    for team_a, team_b in itertools.combinations(teams, 2):
        match = Match.objects.create(
            group=group,
            tournament=group.tournament,
            team_a=team_a,
            team_b=team_b,
            stage='Group'
        )
        matches.append(match)
    return matches


def setup_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    team_count = range(tournament.total_teams)

    if request.method == 'POST':
        team_names = request.POST.getlist('team_names')

        tournament.matches.all().delete()
        tournament.groups.all().delete()
        tournament.teams.all().delete()

        groups = []
        for i in range(tournament.total_groups):
            group_name = chr(ord('A') + i)
            group = Group.objects.create(name=f"Group {group_name}", tournament=tournament)
            groups.append(group)

        for idx, name in enumerate(team_names):
            group = groups[idx % tournament.total_groups]
            Team.objects.create(name=name, tournament=tournament, group=group)

        for group in groups:
            generate_group_fixtures(group)

        return redirect('home')

    return render(request, 'core/setup_tournament.html', {
        'tournament': tournament,
        'team_count': team_count,
    })


def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    groups = tournament.groups.all().prefetch_related('teams', 'matches')

    groups_data = []
    all_group_matches_played = True
    knockout_matches_exist = Match.objects.filter(
        tournament=tournament,
        stage__in=['Quarter', 'Semi', 'Final']
    ).exists()

    for group in groups:
        standings = group.calculate_standings()
        groups_data.append((group, standings))

        if group.matches.filter(played=False).exists():
            all_group_matches_played = False

    # Auto-generate knockout (Quarterfinal) if group stage complete
    if all_group_matches_played and not knockout_matches_exist:
        top_teams = []
        for _, standings in groups_data:
            top_teams.extend([item['team'] for item in standings[:2]])  # Change [:1] for only winners

        for i in range(0, len(top_teams), 2):
            if i + 1 < len(top_teams):
                Match.objects.create(
                    team_a=top_teams[i],
                    team_b=top_teams[i + 1],
                    tournament=tournament,
                    stage='Quarter',
                    played=False
                )

    knockout_matches = Match.objects.filter(
        tournament=tournament,
        stage__in=['Quarter', 'Semi', 'Final']
    ).order_by('stage')

    return render(request, 'core/tournament_detail.html', {
        'tournament': tournament,
        'groups_data': groups_data,
        'knockout_matches': knockout_matches,
    })


def update_match_score(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if request.method == "POST":
        score_a = int(request.POST.get("score_a"))
        score_b = int(request.POST.get("score_b"))
        match.score_a = score_a
        match.score_b = score_b
        match.played = True
        match.save()

        # Group stage point logic
        if match.stage == 'Group':
            team_a = match.team_a
            team_b = match.team_b

            team_a.goals_for += score_a
            team_a.goals_against += score_b
            team_b.goals_for += score_b
            team_b.goals_against += score_a

            if score_a > score_b:
                team_a.points += 3
            elif score_a == score_b:
                team_a.points += 1
                team_b.points += 1
            else:
                team_b.points += 3

            team_a.save()
            team_b.save()

        return redirect("tournament_detail", tournament_id=match.tournament.id)

    return render(request, "core/update_match_score.html", {"match": match})
