from django.urls import path, include
from . import views

urlpatterns = [
    path("play", views.play),
    path("start_game", views.start_game),
    path("answer_question", views.answer_question)
]