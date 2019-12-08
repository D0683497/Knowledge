from django.urls import path, include

from . import views

urlpatterns = [
    path('play', views.play, name='play'),
    path('start_game', views.game, name='game'),
]
