from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.cache import cache
from django.db.models import Max

from .models import Question, Option

import json
import pickle
import random

@login_required
def play(request):
    return render(request, "play.html", {})

@login_required
def game(request):
    username = request.user.username
    if cache.get(username+'round'): #在回合內
        if cache.get(username+'round') == 5: #回合結束
            cache.delete(username+'round')
            return render(request, "result.html", {})
        else:
            cache.incr(username+'round') #增加回合數
            cache.set(username, pickle.dumps(get_random_question()), 10) #隨機拿一題，並設置時間
            return render(request, "game.html", {})
    else: #不再回合內
        cache.set(username+'round', 1, 300) #設置回合
        cache.set(username, pickle.dumps(get_random_question()), 10) #隨機拿一題，並設置時間
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
    return JsonResponse(data)

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
@login_required
def answer(request):
    username = request.user.username
    if cache.get(username): # 時間內回答
        select_option = request.POST.get('option')
        return HttpResponseRedirect(reverse('game'))
    else: # 時間外回答
        print('timeout')
        return HttpResponseRedirect(reverse('game'))

