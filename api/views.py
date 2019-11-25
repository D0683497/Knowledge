from django.shortcuts import render
from rest_framework import viewsets
from .models import ExtendUser

from .serializer import ExtendUserSerializer

class ExtendUserViewSet(viewsets.ModelViewSet):
    queryset = ExtendUser.objects.all()
    serializer_class = ExtendUserSerializer
