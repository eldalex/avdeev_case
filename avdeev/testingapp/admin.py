from django.contrib import admin
from .models import Tests
from .models import Testquestion
from .models import Answers
from django import forms
from django.core.exceptions import ValidationError


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ('question_id', 'aswer_text', 'true_answer',)
        readonly_fields = ('question_id',)

    def clean(self):
        cleaned_data = super().clean()
        true_answer = cleaned_data.get("true_answer")
        if true_answer:
            # Проверяем, что у других ответов не установлен чекбокс "Верный ответ"
            answers = Answers.objects.filter(question_id=cleaned_data.get("question_id"))
            for answer in answers:
                if answer.true_answer:
                    raise ValidationError("Нельзя установить более одного верного ответа")
        return cleaned_data


# Register your models here.
class AnswerAdm(admin.StackedInline):
    form = AnswerForm
    model = Answers
    fields = ('question_id', 'aswer_text', 'true_answer',)
    readonly_fields = ('question_id',)


class TestsAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'test_name');
    list_display_links = ('test_name',)

    def save(self, *args, **kwargs):
        print('TestsAdmin')
        super(TestsAdmin, self).save(*args, **kwargs)


class UserModelForm(forms.ModelForm):

    def question_text(self):
        data = self.cleaned_data['question_text']
        if data is None:
            raise ValidationError('ERROR question_text')
        return data


class TestquestionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'test_id', 'question_text',)
    list_display_links = ('question_id',)
    inlines = [AnswerAdm, ]

    # def test_valid(self,request):
    #     for item in request.POST:
    #         if "aswer_text" in item and request.POST[item] != '':
    #             if request.POST[item] == '111':
    #                 return False
    #
    # def save_formset(self, request, form, formset, change):
    #     print('ssas')
    #     if self.test_valid(request):
    #         if self.test_valid(request):
    #             formset.save()
    #             if not change:
    #                 for f in formset.forms:
    #                     obj = f.instance
    #                     obj.user = request.user
    #                     obj.save()
    #     else:
    #         raise ValidationError('ERROR salary number!')


admin.site.register(Tests, TestsAdmin)
admin.site.register(Testquestion, TestquestionAdmin)
admin.site.register(Answers)
