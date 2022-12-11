from django.db import models


# Create your models here.
class Tests(models.Model):
    test_id = models.AutoField(verbose_name='id теста', primary_key=True)
    test_name = models.CharField(max_length=200, verbose_name='Наименование')
    test_parent = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name='Предыдущий тест', null=True,
                                    blank=True)

    def __str__(self):
        return self.test_name

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class TestResults(models.Model):
    test_id = models.ForeignKey(Tests, on_delete=models.CASCADE, verbose_name='id теста')
    user_id = models.IntegerField(verbose_name='id пользователя')
    test_is_pass = models.BooleanField(verbose_name='Тест полностью пройден')
    true_answer = models.IntegerField(verbose_name='количество правильных ответов')
    wrong_answer = models.IntegerField(verbose_name='количество не правильных ответов')


class Testquestion(models.Model):
    question_id = models.IntegerField(verbose_name='id вопроса')
    test_id = models.ForeignKey(Tests, on_delete=models.CASCADE, verbose_name='id теста')
    question_text = models.CharField(max_length=200, verbose_name='Текст вопроса')

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answers(models.Model):
    question_id = models.ForeignKey(Testquestion, on_delete=models.CASCADE, verbose_name='id вопроса', unique=True)
    answer_1_text = models.CharField(max_length=200, verbose_name='Текст ответа 1', blank=True, null=True)
    true_answer_1 = models.BooleanField(verbose_name='Верный ответ 1', blank=True)
    answer_2_text = models.CharField(max_length=200, verbose_name='Текст ответа 2', blank=True, null=True)
    true_answer_2 = models.BooleanField(verbose_name='Верный ответ 2', blank=True)
    answer_3_text = models.CharField(max_length=200, verbose_name='Текст ответа 3', blank=True, null=True)
    true_answer_3 = models.BooleanField(verbose_name='Верный ответ 3', blank=True)
    answer_4_text = models.CharField(max_length=200, verbose_name='Текст ответа 4', blank=True, null=True)
    true_answer_4 = models.BooleanField(verbose_name='Верный ответ 4', blank=True)
    answer_5_text = models.CharField(max_length=200, verbose_name='Текст ответа 5', blank=True, null=True)
    true_answer_5 = models.BooleanField(verbose_name='Верный ответ 5', blank=True)
    answer_6_text = models.CharField(max_length=200, verbose_name='Текст ответа 5', blank=True, null=True)
    true_answer_6 = models.BooleanField(verbose_name='Верный ответ 6', blank=True)

    def __str__(self):
        return str(self.question_id)

    def save(self, *args, **kwargs):
        print('Answers')
        super(Answers, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
