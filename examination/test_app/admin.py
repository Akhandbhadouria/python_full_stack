from django.contrib import admin
from .models import Question, Result

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'answer', 'marks')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'marks', 'total_marks', 'date')
    readonly_fields = ('date',)
