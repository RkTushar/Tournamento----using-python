from django.shortcuts import render, redirect, get_object_or_404
from .models import Tournament

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
