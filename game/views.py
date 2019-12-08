from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Question, Option

import json

from django.core.cache import cache
import pickle
from django.db.models import Max
import random

@login_required
def play(request):
    return render(request, "play.html", {})

@login_required
def game(request):
    username = request.user.username
    if request.method == 'POST':
        return render(request, "game.html", {})
    else:
        cache.set(username, pickle.dumps(get_random_question()), 300) # 隨機拿一題
        return render(request, "game.html", {})

"""
獲取問題
"""
@login_required
def question(request):
    username = request.user.username
    q = pickle.loads(cache.get(username))
    data = {}
    data['topic'] = q.topic
    for index, option in enumerate(q.choices.all()):
        data['option'+str(index)] = option.description
    cache.set(username, 'question', 60) # 設置時間
    return JsonResponse(data)
    # 沒驗證回合

def get_random_question():
    max_id = Question.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        id = random.randint(1, max_id)
        question = Question.objects.filter(id=id).first()
        if question:
            return question

"""
驗證回答
"""
"""
@login_required
def answer(request):
    username = request.user.username
    if cache.get(username): # 時間內回答

    else: # 時間外回答
"""
