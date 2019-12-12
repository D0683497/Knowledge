from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.cache import cache
from django.db.models import Max
from django.contrib.auth import get_user_model
from django.core import serializers

from .models import Question, Round, History, ExtendUser, Report

import json
import pickle
import random

"""
usernamequestion: 紀錄題目id
usernameoption: 紀錄選擇的選項
userround: 紀錄回合(一場五回合)，15秒
"""

@login_required
def play(request):
    username = request.user.username
    cache.delete(username+'question')
    cache.delete(username+'option')
    cache.delete(username+'round')
    return render(request, "play.html", {})

@login_required
def game(request):
    username = request.user.username
    cache.delete(username+'question')
    cache.delete(username+'option')
    cache.delete(username+'round')
    return render(request, "game.html", {})

"""
獲取問題
set usernamequestion
set userround 15秒
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
            record_question = pickle.loads(cache.get(username+'question')) #拿取紀錄題目 list
            record_question.append(q.id)
            cache.set(username+'question', pickle.dumps(record_question)) #紀錄拿的題目
            cache.incr(username+'round') #增加回合數
            cache.touch(username+'round', 15)
            data = {
                'message': 'success',
                'topic': q.topic,
                'option_1': q.option_1,
                'option_2': q.option_2,
                'option_3': q.option_3,
                'option_4': q.option_4,
            }
            return JsonResponse(data)
    else: #開始回合
        q = get_random_question()
        record_question = []
        record_question.append(q.id)
        cache.set(username+'question', pickle.dumps(record_question))
        cache.set(username+'round', 1) #設置回合
        cache.touch(username+'round', 15)
        data = {
            'message': 'success',
            'topic': q.topic,
            'option_1': q.option_1,
            'option_2': q.option_2,
            'option_3': q.option_3,
            'option_4': q.option_4,
        }
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
set usernameoption
"""
@login_required
def answer(request):
    username = request.user.username
    if request.method == 'POST':
        if cache.get(username+'round'): # 時間內回答
            select_value = request.POST.get('option')
        else: # 時間外回答
            select_value = 'timeout'

        if cache.get(username+'option'):
            record_option = pickle.loads(cache.get(username+'option')) #拿取紀錄選項 list
        else:
            record_option = []
        
        record_option.append(select_value)
        cache.set(username+'option', pickle.dumps(record_option))
        data = {'message': 'success'}
        return JsonResponse(data)

@login_required
def result(request):   
    return render(request, "result.html", {})

@login_required
def get_result(request):
    username = request.user.username
    record_question = pickle.loads(cache.get(username+'question')) #拿取紀錄題目 list
    record_option = pickle.loads(cache.get(username+'option')) #拿取紀錄選項 list
    round_lst = []

    if len(record_question) == 5 and len(record_option) == 5:
        total_score = 0
        for i in range(5):
            question = Question.objects.filter(id=record_question[i]).first()
            if question.correct_option == record_option[i]:
                total_score = total_score + 1
            oneround = Round(question=question, select_option=record_option[i])
            oneround.save()
            round_lst.append(oneround)
        
        history = History(score=total_score)
        history.save()
        for i in round_lst:
            history.record.add(i)
            history.save()

        user = ExtendUser.objects.filter(username=username).first()
        user.history.add(history)
        user.save()

        data = {
            'message': '挑戰成功',
            'time' :history.created_at,
            'score': history.score,
            'question': [
                {
                    'topic': history.record.all()[0].question.topic,
                    'solution': history.record.all()[0].question.solution,
                    'option_1': history.record.all()[0].question.option_1,
                    'option_2': history.record.all()[0].question.option_2,
                    'option_3': history.record.all()[0].question.option_3,
                    'option_4': history.record.all()[0].question.option_4,
                    'correct_option': history.record.all()[0].question.correct_option,
                    'select_option': history.record.all()[0].select_option,
                },
                {
                    'topic': history.record.all()[1].question.topic,
                    'solution': history.record.all()[1].question.solution,
                    'option_1': history.record.all()[1].question.option_1,
                    'option_2': history.record.all()[1].question.option_2,
                    'option_3': history.record.all()[1].question.option_3,
                    'option_4': history.record.all()[1].question.option_4,
                    'correct_option': history.record.all()[1].question.correct_option,
                    'select_option': history.record.all()[1].select_option,
                },
                {
                    'topic': history.record.all()[2].question.topic,
                    'solution': history.record.all()[2].question.solution,
                    'option_1': history.record.all()[2].question.option_1,
                    'option_2': history.record.all()[2].question.option_2,
                    'option_3': history.record.all()[2].question.option_3,
                    'option_4': history.record.all()[2].question.option_4,
                    'correct_option': history.record.all()[2].question.correct_option,
                    'select_option': history.record.all()[2].select_option,
                },
                {
                    'topic': history.record.all()[3].question.topic,
                    'solution': history.record.all()[3].question.solution,
                    'option_1': history.record.all()[3].question.option_1,
                    'option_2': history.record.all()[3].question.option_2,
                    'option_3': history.record.all()[3].question.option_3,
                    'option_4': history.record.all()[3].question.option_4,
                    'correct_option': history.record.all()[3].question.correct_option,
                    'select_option': history.record.all()[3].select_option,
                },
                {
                    'topic': history.record.all()[4].question.topic,
                    'solution': history.record.all()[4].question.solution,
                    'option_1': history.record.all()[4].question.option_1,
                    'option_2': history.record.all()[4].question.option_2,
                    'option_3': history.record.all()[4].question.option_3,
                    'option_4': history.record.all()[4].question.option_4,
                    'correct_option': history.record.all()[4].question.correct_option,
                    'select_option': history.record.all()[4].select_option,
                }
            ]
        }

        cache.delete(username+'question')
        cache.delete(username+'option')
        cache.delete(username+'round')
        return JsonResponse(data)
    else:
        cache.delete(username+'question')
        cache.delete(username+'option')
        cache.delete(username+'round')
        data = {'message': '挑戰失敗'}
        return JsonResponse(data)

@login_required
def report(request):
    user = request.user
    if request.method == 'POST':
        topic = request.POST.get('topic')
        description = request.POST.get('description')
        if topic and description:
            question = Question.objects.filter(topic=topic).first()
            Report.objects.create(question=question, user=user, description=description)
            data = {'message': 'success'}
            return JsonResponse(data)
        else:
            data = {'message': 'fail'}
            return JsonResponse(data)
