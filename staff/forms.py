from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

class AwardForm(forms.Form):
    nid = forms.CharField(required=True, 
        error_messages={'required': '此欄位必須填寫'}, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '請輸入欲簽到之學號'}),
        label="學號")
