from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from game.models import ExtendUser
from .forms import SignUpForm, ManageForm

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def manage(request):
    user = ExtendUser.objects.filter(username=request.user.username).first()
    if request.method == 'POST':
        form = ManageForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'registration/manage.html', {'form': form})
    else:
        form = ManageForm(instance=user)
    return render(request, 'registration/manage.html', {'form': form})
