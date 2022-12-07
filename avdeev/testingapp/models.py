from django.db import models


# Create your models here.
class Tests(models.Model):
    test_id = models.AutoField(verbose_name='id теста', primary_key=True)
    test_name = models.CharField(max_length=200, verbose_name='Наименование')

    def __str__(self):
        return self.test_name

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Testquestion(models.Model):
    question_id = models.IntegerField(verbose_name='id вопроса')
    test_id = models.ForeignKey(Tests, on_delete=models.CASCADE, verbose_name='id теста')
    question_text = models.CharField(max_length=200, verbose_name='Текст вопроса')
    question_answers = models.CharField(max_length=200, verbose_name='Варианты ответов')
    question_true_answers = models.CharField(max_length=200, verbose_name='Верный ответ')

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answers(models.Model):
    question_id = models.ForeignKey(Testquestion, on_delete=models.CASCADE, verbose_name='id вопроса')
    aswer_text = models.CharField(max_length=200, verbose_name='Текст ответа')
    true_answer = models.BooleanField(verbose_name='Верный ответ')

    def __str__(self):
        return self.aswer_text

    def save(self, *args, **kwargs):

        print('Answers')
        super(Answers, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
