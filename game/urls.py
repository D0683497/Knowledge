from django.urls import path, include
from . import views

urlpatterns = [
    path('play', views.play),
    path('get_question', views.get_question)
]