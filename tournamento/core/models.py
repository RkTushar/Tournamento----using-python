from django.db import models

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    total_teams = models.PositiveIntegerField()
    total_groups = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True, related_name='teams')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=10)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return f"{self.name} - {self.tournament.name}"

    def calculate_standings(self):
        """
        Calculate standings for the group based on match results.
        """
        standings = []

        for team in self.teams.all():
            team_stats = {
                'team': team,
                'points': 0,
                'goals_for': 0,
                'goals_against': 0,
                'matches_played': 0,
            }

            for match in self.matches.all():
                if match.played:
                    if match.team_a == team:
                        team_stats['goals_for'] += match.score_a
                        team_stats['goals_against'] += match.score_b
                        team_stats['matches_played'] += 1
                        if match.score_a > match.score_b:
                            team_stats['points'] += 3
                        elif match.score_a == match.score_b:
                            team_stats['points'] += 1

                    elif match.team_b == team:
                        team_stats['goals_for'] += match.score_b
                        team_stats['goals_against'] += match.score_a
                        team_stats['matches_played'] += 1
                        if match.score_b > match.score_a:
                            team_stats['points'] += 3
                        elif match.score_a == match.score_b:
                            team_stats['points'] += 1

            standings.append(team_stats)

        standings.sort(
            key=lambda x: (-x['points'], -(x['goals_for'] - x['goals_against']), -x['goals_for']),
        )

        return standings


class Match(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='matches')
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_a_matches')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_b_matches')
    score_a = models.IntegerField(default=0)
    score_b = models.IntegerField(default=0)
    played = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team_a.name} vs {self.team_b.name}"

