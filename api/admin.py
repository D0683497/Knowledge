from django.contrib import admin
from .models import ExtendUser, Question
from .forms import ExtendUserAdminForm, QuestionAdminForm

# Register your models here.

class ExtendUserAdmin(admin.ModelAdmin):
    form = ExtendUserAdminForm
    search_fields = ('studentId',)

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    search_fields = ('topic',)

admin.site.register(ExtendUser, ExtendUserAdmin)
admin.site.register(Question, QuestionAdmin)
