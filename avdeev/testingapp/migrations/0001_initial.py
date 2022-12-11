# Generated by Django 4.1.3 on 2022-12-11 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tests',
            fields=[
                ('test_id', models.AutoField(primary_key=True, serialize=False, verbose_name='id теста')),
                ('test_name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('test_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='testingapp.tests', verbose_name='Предыдущий тест')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
            },
        ),
        migrations.CreateModel(
            name='TestResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(verbose_name='id пользователя')),
                ('test_is_pass', models.BooleanField(verbose_name='Тест полностью пройден')),
                ('true_answer', models.IntegerField(verbose_name='количество правильных ответов')),
                ('wrong_answer', models.IntegerField(verbose_name='количество не правильных ответов')),
                ('test_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testingapp.tests', verbose_name='id теста')),
            ],
        ),
        migrations.CreateModel(
            name='Testquestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.IntegerField(verbose_name='id вопроса')),
                ('question_text', models.CharField(max_length=200, verbose_name='Текст вопроса')),
                ('test_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testingapp.tests', verbose_name='id теста')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_1_text', models.CharField(blank=True, max_length=200, null=True, verbose_name='Текст ответа 1')),
                ('true_answer_1', models.BooleanField(blank=True, verbose_name='Верный ответ 1')),
                ('answer_2_text', models.CharField(blank=True, max_length=200, null=True, verbose_name='Текст ответа 2')),
                ('true_answer_2', models.BooleanField(blank=True, verbose_name='Верный ответ 2')),
                ('answer_3_text', models.CharField(blank=True, max_length=200, null=True, verbose_name='Текст ответа 3')),
                ('true_answer_3', models.BooleanField(blank=True, verbose_name='Верный ответ 3')),
                ('answer_4_text', models.CharField(blank=True, max_length=200, null=True, verbose_name='Текст ответа 4')),
                ('true_answer_4', models.BooleanField(blank=True, verbose_name='Верный ответ 4')),
                ('answer_5_text', models.CharField(blank=True, max_length=200, null=True, verbose_name='Текст ответа 5')),
                ('true_answer_5', models.BooleanField(blank=True, verbose_name='Верный ответ 5')),
                ('answer_6_text', models.CharField(blank=True, max_length=200, null=True, verbose_name='Текст ответа 5')),
                ('true_answer_6', models.BooleanField(blank=True, verbose_name='Верный ответ 6')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testingapp.testquestion', unique=True, verbose_name='id вопроса')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
    ]