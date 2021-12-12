from django.contrib import admin
from .models import Poll, Question, Choices, UserPollAnswer, UserQuestionAnswer

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choices)
admin.site.register(UserQuestionAnswer)
admin.site.register(UserPollAnswer)
# Register your models here.
