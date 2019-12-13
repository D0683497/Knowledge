from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm

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
    return render(request, 'registration/manage.html', {})
