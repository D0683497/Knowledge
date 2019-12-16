from django.shortcuts import render

def act(request):
    return render(request, "act.html", {})
