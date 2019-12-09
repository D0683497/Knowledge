from django.contrib import admin

from .models import ExtendUser, Question, Option, Record, History

# Register your models here.

class HistoryInline(admin.TabularInline):
    model = History

class ExtendUserAdmin(admin.ModelAdmin):
    search_fields = ('studentId',)
    inlines = [HistoryInline,]

class OptionInline(admin.TabularInline):
    model = Option

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ('topic',)
    inlines = [OptionInline, ]

class HistoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(ExtendUser, ExtendUserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Record)
