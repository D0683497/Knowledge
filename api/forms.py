from django import forms
from .models import ExtendUser, Question

class ExtendUserAdminForm(forms.ModelForm):
    class Meta:
        model = ExtendUser
        fields = '__all__'

class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'