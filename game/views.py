from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils.safestring import mark_safe

from .models import Question, Option

import json

@login_required
def play(request):
    return render(request, "play.html", {})

@login_required
def game(request):
    username = request.user.username
    return render(request, "game.html", {'username': mark_safe(json.dumps(username))})
    #return render(request, 'chat/room.html', {'room_name_json': mark_safe(json.dumps(room_name))})
