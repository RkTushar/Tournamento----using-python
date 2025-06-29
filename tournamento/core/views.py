from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # ✅ NEW
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
            team_a=team_a,
            team_b=team_b,
            stage='Group',
            tournament=group.tournament
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
    for group in groups:
        standings = group.calculate_standings()
        groups_data.append((group, standings))
        if group.matches.filter(played=False).exists():
            all_group_matches_played = False

    knockout_matches = Match.objects.filter(tournament=tournament, stage__in=['Quarter', 'Semi', 'Final'])

    # Auto-generate Quarterfinals
    if all_group_matches_played and not knockout_matches.filter(stage='Quarter').exists():
        top_teams = []
        for _, standings in groups_data:
            top_teams.extend([item['team'] for item in standings[:2]])

        for i in range(0, len(top_teams), 2):
            if i + 1 < len(top_teams):
                Match.objects.create(
                    team_a=top_teams[i],
                    team_b=top_teams[i + 1],
                    tournament=tournament,
                    stage='Quarter'
                )

    # Auto-generate Semifinals
    quarterfinals = knockout_matches.filter(stage='Quarter', played=True)
    if quarterfinals.count() == 4 and not knockout_matches.filter(stage='Semi').exists():
        winners = []
        for match in quarterfinals:
            if match.score_a > match.score_b:
                winners.append(match.team_a)
            else:
                winners.append(match.team_b)

        for i in range(0, len(winners), 2):
            if i + 1 < len(winners):
                Match.objects.create(
                    team_a=winners[i],
                    team_b=winners[i + 1],
                    tournament=tournament,
                    stage='Semi'
                )

    # Auto-generate Final
    semifinals = knockout_matches.filter(stage='Semi', played=True)
    if semifinals.count() == 2 and not knockout_matches.filter(stage='Final').exists():
        finalists = []
        for match in semifinals:
            if match.score_a > match.score_b:
                finalists.append(match.team_a)
            else:
                finalists.append(match.team_b)

        if len(finalists) == 2:
            Match.objects.create(
                team_a=finalists[0],
                team_b=finalists[1],
                tournament=tournament,
                stage='Final'
            )

    updated_knockouts = Match.objects.filter(
        tournament=tournament,
        stage__in=['Quarter', 'Semi', 'Final']
    ).order_by('stage')

    final_match = updated_knockouts.filter(stage='Final', played=True).first()
    winner = None
    if final_match:
        if final_match.score_a > final_match.score_b:
            winner = final_match.team_a
        elif final_match.score_b > final_match.score_a:
            winner = final_match.team_b

    return render(request, 'core/tournament_detail.html', {
        'tournament': tournament,
        'groups_data': groups_data,
        'knockout_matches': updated_knockouts,
        'winner': winner,
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

        messages.success(request, "✅ Score updated successfully!")  # ✅ Message
        return redirect("update_match_score", match_id=match.id)  # Stay on page to see message

    return render(request, "core/update_match_score.html", {"match": match})
