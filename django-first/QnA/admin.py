from django.contrib import admin
# admin 페이지에 Question 메뉴 추가
from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)

