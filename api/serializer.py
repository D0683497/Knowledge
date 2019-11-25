from rest_framework import serializers
from .models import ExtendUser


# Serializers define the API representation.
class ExtendUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExtendUser
        fields = ['username', 'email', 'is_staff']
