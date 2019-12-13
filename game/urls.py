from django.urls import path, include

from . import views

urlpatterns = [
    path('play', views.play, name='play'),
    path('start_game', views.game, name='game'),
    path('get_question', views.question, name='question'),
    path('answer', views.answer, name='answer'),
    path('result', views.result, name='result'),
    path('get_result', views.get_result, name='get_result'),
    path('report', views.report, name='report'),
    path('rank', views.rank, name='rank'),
    path('get_rank', views.get_rank, name='get_rank'),
]
