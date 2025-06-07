import random
from .models import Group, Team, Match

def assign_groups_and_generate_fixtures(tournament):
    # Clear existing data (optional, if re-generating)
    tournament.groups.all().delete()

    # Create groups
    groups = []
    for i in range(tournament.total_groups):
        group = Group.objects.create(
            name=f"Group {chr(65 + i)}",  # A, B, C...
            tournament=tournament
        )
        groups.append(group)

    # Shuffle teams randomly and assign to groups
    teams = list(tournament.teams.all())
    random.shuffle(teams)
    
    for index, team in enumerate(teams):
        group = groups[index % len(groups)]
        team.group = group
        team.save()

    # Generate matches (round robin) within each group
    for group in groups:
        group_teams = list(group.teams.all())
        for i in range(len(group_teams)):
            for j in range(i + 1, len(group_teams)):
                Match.objects.create(
                    group=group,
                    team_a=group_teams[i],
                    team_b=group_teams[j],
                )
