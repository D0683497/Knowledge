from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Question

# Create your views here.

@login_required
def play(request):
    return render(request, 'play.html', {})

def get_question(request):
    questions = Question.objects.all()
    json = []
    for question in questions:
        choices = question.choices.all()
        options = [option.description for option in choices]
        json.append({
            "topic": question.topic,
            "option": options
        })
    return JsonResponse(json, safe=False)