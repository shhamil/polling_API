# Generated by Django 3.1 on 2021-12-12 17:53

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poll_name', models.TextField(verbose_name='Название')),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='UserPollAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='ID пользователя')),
                ('poll', models.IntegerField(verbose_name='ID опроса')),
            ],
        ),
        migrations.CreateModel(
            name='UserQuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.IntegerField()),
                ('question_text', models.TextField()),
                ('answer', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polling_API.userpollanswer', verbose_name='Опрос')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(blank=True, verbose_name='Текст вопроса')),
                ('question_type', models.IntegerField(blank=True, choices=[(1, 'Текстовый ответ'), (2, 'Выбор одного варианта'), (3, 'Выбор одного/нескольких вариантов')], verbose_name='Тип вопроса')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polling_API.poll', verbose_name='Опрос')),
            ],
        ),
        migrations.CreateModel(
            name='Choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choices_options', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), size=None)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polling_API.question', verbose_name='Вопрос')),
            ],
        ),
    ]
