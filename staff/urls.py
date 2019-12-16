from django.urls import path, include

from . import views


urlpatterns = [
    path('award', views.award, name='award'),
]
