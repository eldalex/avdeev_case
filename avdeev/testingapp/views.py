from django.db.models import Max
import json
from django.shortcuts import redirect
from .models import Tests, Testquestion, Answers, TestResults
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from django.contrib.auth import logout
from django.db.models import Q


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response = redirect(f'http://{request.headers["Host"]}/test/appfortests')
                    return response
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        response = redirect(f'http://{request.headers["Host"]}/test/success/')
        return response
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def logoutuser(request):
    logout(request)
    response = redirect(f'http://{request.headers["Host"]}/')
    return response


def start_index(request):
    return render(request, './index.html')


def first_page_tests(request):
    if request.user.username == '':
        response = redirect(f"http://{request.headers['Host']}/test/login/")
        return response
    else:
        user_pass_test = TestResults.objects.values('test_id', 'test_is_pass').filter(user_id=request.user.id)
        user_pass_test_list = []
        for item in user_pass_test:
            if item['test_is_pass']:
                user_pass_test_list.append(item['test_id'])

        pass_tests = Tests.objects.filter(test_id__in=user_pass_test_list)
        not_pass_test = Tests.objects.filter(
            Q(test_parent__in=user_pass_test_list) | Q(test_parent__isnull=True)).exclude(
            test_id__in=user_pass_test_list, )
        obj = {'pass_tests': pass_tests,
               'not_pass_tests': not_pass_test}
        return render(request, './index_tests.html', obj)


# Q(test_parent__in=user_pass_test_list) | Q(test_parent__nullis=True)

def get_statistics(request):
    testID = int(json.loads(request.body.decode('utf-8'))['test_id'])
    userID = request.user.id
    if TestResults.objects.filter(test_id=testID, user_id=userID).exists():
        data = TestResults.objects.get(test_id=testID, user_id=userID)
        response_data = {
            "true": f"{data.true_answer or 0}",
            "false": f"{data.wrong_answer or 0}",
            "true_pers": f"{round(100 * (data.true_answer / (data.true_answer + data.wrong_answer))) or 0}%"
        }
    else:
        response_data = {
            "true": "0",
            "false": "0",
            "true_pers": "0%"
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def testing_page(request, test_id=0):
    if request.user.username == '':
        response = redirect(f'http://{request.headers["Host"]}/login/')
        return response
    else:
        test_id = test_id
        test_name = Tests.objects.get(pk=test_id).test_name
        test_question = Testquestion.objects.all().filter(test_id=test_id, question_id=1).first()
        obj = {
            "testID": test_id,
            "testName": test_name,
            "number": 1,
            "question": test_question.question_text,
        }
        return render(request, './testing.html', obj)


def get_next_question(test_id, question_number, user_id):
    max_question = Testquestion.objects.filter(test_id=test_id).aggregate(Max('question_id'))
    if question_number <= max_question["question_id__max"]:
        next_question = Testquestion.objects.get(test_id=test_id, question_id=question_number)
        answers_for_question = list(Answers.objects.filter(id=next_question.id).values())[0]
        num = 1
        ans = {}
        for i in answers_for_question:
            if "_text" in i and answers_for_question[i] is not None:
                ans.update({num: answers_for_question[i]})
                num += 1
        obj = {
            "testID": test_id,
            "number": next_question.question_id,
            "question": next_question.question_text,
            "realQuestionId": answers_for_question["id"],
            "answers": ans
        }
    else:
        set_test_is_pass(test_id, user_id)
        obj = {"finish": "true"}
    return obj


def success_page(request):
    return render(request, './successpage.html')


def set_test_is_pass(test_id, user_id):
    if TestResults.objects.filter(test_id=test_id, user_id=user_id).exists():
        result = TestResults.objects.get(test_id=test_id, user_id=user_id)
        result.test_is_pass = True
        result.save()


def check_and_record_answer(answers, test_id, question_number, user_id, realQuestionId):
    answers_for_question = list(Answers.objects.filter(id=realQuestionId).values())[0]
    true_answers = []
    for i in answers_for_question:
        if "_text" in i and answers_for_question[i] is not None:
            if answers_for_question[f"true_answer_{i[7]}"]:
                true_answers.append(str(i[7]))
    test = Tests.objects.get(pk=test_id)
    if TestResults.objects.filter(test_id=test_id, user_id=user_id).exists():
        result = TestResults.objects.get(test_id=test_id, user_id=user_id)
    else:
        result = TestResults(test_id=test, user_id=user_id, test_is_pass=False, true_answer=0, wrong_answer=0)
        result.save()
    if question_number == 1:
        result.true_answer = 0
        result.wrong_answer = 0
        result.save()

    if answers == true_answers:
        result.true_answer += 1
        result.save()
    else:
        result.wrong_answer += 1
        result.save()


def get_question_response(request):
    response_data = {}
    request_body = json.loads(request.body.decode('utf-8'))
    if "test_id" in request_body and request_body['test_id'] != "":
        test_id = request_body['test_id']
    else:
        test_id = None
    if "question_number" in request_body and request_body['question_number'] != "":
        question_number = int(request_body['question_number'])
    else:
        question_number = None
    if "answers" in request_body:
        answers = request_body['answers']
    else:
        answers = None
    if "realQuestionId" in request_body:
        realQuestionId = request_body['realQuestionId']
    else:
        realQuestionId = None

    if answers and test_id and question_number:
        check_and_record_answer(answers, test_id, question_number, request.user.id, realQuestionId)
        response_data = get_next_question(test_id, question_number + 1, request.user.id)
    elif test_id and question_number:
        response_data = get_next_question(test_id, question_number, request.user.id)
    else:
        pass
    return HttpResponse(json.dumps(response_data), content_type="application/json")
