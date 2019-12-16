from django.urls import path, include

from . import views

urlpatterns = [
    path('108', views.info108, name='info108'),
]
