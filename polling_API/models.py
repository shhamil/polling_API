from django.db import models
from django.contrib.postgres.fields import ArrayField

QUESTION_TYPE = (
    (1, 'Текстовый ответ'),
    (2, 'Выбор одного варианта'),
    (3, 'Выбор одного/нескольких вариантов'),
)


class Poll(models.Model):
    poll_name = models.TextField(verbose_name='Название')
    start_date = models.DateField(auto_now_add=True, verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.poll_name


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name='Опрос')
    question_text = models.TextField(verbose_name='Текст вопроса', blank=True)
    question_type = models.IntegerField(choices=QUESTION_TYPE, verbose_name='Тип вопроса', blank=True)

    def __str__(self):
        return self.question_text


class Choices(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    choices_options = ArrayField(models.TextField(blank=True, null=True))

    def __str__(self):
        return self.choices_options[1]


class UserPollAnswer(models.Model):
    user_id = models.IntegerField(verbose_name='ID пользователя')
    poll = models.IntegerField(verbose_name="ID опроса")


class UserQuestionAnswer(models.Model):
    poll = models.ForeignKey(UserPollAnswer, on_delete=models.CASCADE, verbose_name='Опрос')
    question_id = models.IntegerField()
    question_text = models.TextField()
    answer = ArrayField(models.TextField())




