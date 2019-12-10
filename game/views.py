from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.cache import cache
from django.db.models import Max

from .models import Question, Option, Record, History

import json
import pickle
import random

"""
usernamequestion: 紀錄一題題目及選項
userround: 紀錄回合(一場五回合)
userrecord: 紀錄答題記錄(用 list 的形式)
"""

@login_required
def play(request):
    username = request.user.username
    if cache.get(username+'round'):
        cache.delete(username+'round')
        cache.delete(username)
        cache.delete(username+'record')
    return render(request, "play.html", {})

@login_required
def game(request):
    username = request.user.username
    if cache.get(username+'round'): #之前中離遊戲
        return render(request, "game.html", {})
    else:
        return render(request, "game.html", {})

"""
獲取問題
"""
@login_required
def question(request):
    username = request.user.username

    if cache.get(username+'round'): #回合中
        if cache.get(username+'round') == 5: #回合結束
            cache.delete(username+'round')
            data = {'message': 'result'}
            return JsonResponse(data)
        else:
            q = get_random_question()
            cache.incr(username+'round') #增加回合數
            cache.set(username, pickle.dumps(q), 13) #隨機拿一題，並設置時間
            data = {}
            data['message'] = 'success'
            data['topic'] = q.topic
            for index, option in enumerate(q.choices.all()):
                data['option'+str(index)] = option.description
            return JsonResponse(data)
    else: #開始回合
        q = get_random_question()
        cache.set(username+'round', 1, 300) #設置回合
        cache.set(username, pickle.dumps(q), 13) #隨機拿一題，並設置時間
        data = {}
        data['message'] = 'success'
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
    if request.method == 'POST':
        if cache.get(username): # 時間內回答
            select_value = request.POST.get('option')
            question = pickle.loads(cache.get(username))
            cache.delete(username)
            select_option = question.choices.all().filter(description=select_value).first()
            if cache.get(username+'record'): #如果有對戰紀錄
                r = pickle.loads(cache.get(username+'record'))
                r.append(select_option)
                cache.set(username+'record', pickle.dumps(r), 15)
            else:
                r = []
                r.append(select_option)
                cache.set(username+'record', pickle.dumps(r), 15)
            data = {'message': 'success'}
            return JsonResponse(data)
        else: # 時間外回答
            cache.delete(username+'round')
            cache.delete(username)
            cache.delete(username+'record')
            data = {'error': '請尊重遊戲規則'}
            return JsonResponse(data)

@login_required
def result(request):
    username = request.user.username
    if cache.get(username+'record'): #有紀錄
        r = pickle.loads(cache.get(username+'record')) #選項紀錄
        if len(r) == 5:
            total_score = 0
            record = Record()
            record.save()
            for i in r:
                total_score = total_score + i.score #算分數
                record.options.add(i)
                record.save()
            if History.objects.filter(user=request.user).exists(): #之前有玩過，有紀錄
                history = History.objects.filter(user=request.user).first()
            else:
                history = History(user=request.user)
                history.save()
            history.records.add(record)
            history.save()
            cache.delete(username+'round')
            cache.delete(username)
            cache.delete(username+'record')
            return render(request, "result.html", {'record': record})
        else:
            cache.delete(username+'round')
            cache.delete(username)
            cache.delete(username+'record')
            return render(request, "result.html", {'fail': "挑戰失敗"})
    else: # 沒紀錄
        cache.delete(username+'round')
        cache.delete(username)
        cache.delete(username+'record')
        return render(request, "result.html", {'fail': "發生錯誤"})
