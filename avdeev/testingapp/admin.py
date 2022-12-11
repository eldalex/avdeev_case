from django.contrib import admin
from .models import Tests, Testquestion, Answers
from django import forms
from django.core.exceptions import ValidationError


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ('question_id', 'answer_1_text', 'true_answer_1', 'answer_2_text', 'true_answer_2', 'answer_3_text',
                  'true_answer_3', 'answer_4_text', 'true_answer_4', 'answer_5_text', 'true_answer_5', 'answer_6_text',
                  'true_answer_6',)
        readonly_fields = ('question_id',)

    def clean(self):
        cleaned_data = super().clean()
        count_answers = 0
        count_true = 0
        for i in range(1, 7):
            if cleaned_data[f"answer_{i}_text"] is not None:
                count_answers += 1
                if cleaned_data[f"true_answer_{i}"]:
                    count_true += 1
        if count_answers == count_true:
            raise ValidationError("Все ответы не могут быть верными")
        elif count_answers > 0 and count_true == 0:
            raise ValidationError("Вы не отметили ни один верный вариант")

        return cleaned_data


# Register your models here.
class AnswerAdm(admin.StackedInline):
    form = AnswerForm
    model = Answers
    fields = ('question_id', 'answer_1_text', 'true_answer_1', 'answer_2_text', 'true_answer_2', 'answer_3_text',
              'true_answer_3', 'answer_4_text', 'true_answer_4', 'answer_5_text', 'true_answer_5', 'answer_6_text',
              'true_answer_6',)
    readonly_fields = ('question_id',)

class QuestionInLine(admin.StackedInline):
    model = Testquestion
    fields = ('question_id','test_id','question_text')
    extra = 0


class TestsAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'test_name');
    list_display_links = ('test_name',)
    inlines = [QuestionInLine, ]

    def save(self, *args, **kwargs):
        print('TestsAdmin')
        super(TestsAdmin, self).save(*args, **kwargs)


class TestquestionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'test_id', 'question_text',)
    list_display_links = ('question_id', 'question_text',)
    inlines = [AnswerAdm, ]


admin.site.register(Tests, TestsAdmin)
admin.site.register(Testquestion, TestquestionAdmin)
admin.site.register(Answers)
