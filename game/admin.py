from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import ExtendUser, Question, Round, History
from .resources import QuestionResource

class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource

admin.site.register(ExtendUser)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Round)
admin.site.register(History)
