from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from game.models import ExtendUser

class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = ExtendUser
        fields = ('username', 'password1', 'password2', 'studentId',)

    def clean_studentId(self):
        studentId = self.cleaned_data['studentId'].upper()
        if studentId.isalnum(): #驗證是否只有字母或數字
            return studentId
        else:
            raise ValidationError("學號的格式怪怪的")

class ManageForm(ModelForm):
    class Meta:
        model = ExtendUser
        fields = ('username', 'first_name', 'last_name', 'email', 'studentId')
