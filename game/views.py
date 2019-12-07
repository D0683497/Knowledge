from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import Game, Question, Option

# Create your views here.

@login_required
def play(request):
    return render(request, "play.html", {})

@login_required
def start_game(request):
    user = request.user
    try:
        user.game.delete()
    except Game.DoesNotExist:
        pass
    game = Game.objects.create(user=user)
    json = {"game_id": game.id, "question": []}
    for question in Question.objects.all().order_by("?")[:5]:
        question.game.add(game)
        choices = question.choices.all()
        options = [option.description for option in choices]
        json["question"].append({
            "id": question.id,
            "topic": question.topic,
            "option": options
        })
    return JsonResponse(json)

@login_required
def answer_question(request):
    game_id = request.GET.get("game_id")
    question_id = request.GET.get("question_id")
    option_id = request.GET.get("option_id")
    game = get_object_or_404(Game, id=game_id)
    question = get_object_or_404(Question, id=question_id)
    questions = game.questions.all()
    if game.user != request.user or question not in questions:
        raise PermissionDenied()
    option = get_object_or_404(Option, id=option_id)
    if option.score > 0:
        return HttpResponse("Y")
    else:
        return HttpResponse("N")