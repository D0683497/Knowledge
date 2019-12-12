from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import SignUpForm

def index(request):
    return render(request, 'index.html', {})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = SignUpForm()
        print(form.non_field_errors())
    return render(request, 'registration/register.html', {'form': form})

"""
def error_400(request, exception):
    return render(request,'errors/400.html', {})

def error_403(request, exception):
    return render(request,'errors/403.html', {})

def error_404(request, exception):
    return render(request,'errors/404.html', {})

def error_500(request):
    return render(request,'errors/500.html', {})

def csrf_failure(request, reason=""):
    return render(request,'errors/403_csrf.html', {})
"""