from django import forms
from .models import Tournament, Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']
