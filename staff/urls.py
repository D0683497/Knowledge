from django.urls import path, include

from . import views


urlpatterns = [
    path('search', views.search, name='search'),
    path('detail/<str:nid>', views.detail, name="detail"),
    path('checkin/<str:nid>', views.checkin, name="checkin"),
    path('prize/<str:nid>', views.prize, name="prize"),
]
