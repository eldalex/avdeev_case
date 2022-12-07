from django.shortcuts import render
from django.db.models import Max
import json
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Tests, Testquestion
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from django.contrib.auth import logout


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
                    response = redirect('http://127.0.0.1:8000/')
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
        response = redirect('http://127.0.0.1:8000/success/')
        return response
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def logoutuser(request):
    logout(request)
    response = redirect('http://127.0.0.1:8000/')
    return response


def first_page(request):
    if request.user.username == '':
        response = redirect('http://127.0.0.1:8000/account/login/')
        return response
    else:
        tests = Tests.objects.all()
        obj = {'tests': tests}
        print("stop")

        return render(request, './index.html', obj)


def testing_page(request, test_id=0):
    if request.user.username == '':
        response = redirect('http://127.0.0.1:8000/account/login/')
        return response
    else:
        test_id = test_id
        test_question = Testquestion.objects.all().filter(test_id=test_id, question_id=1).first()
        obj = {
            "testID": test_id,
            "number": 1,
            "question": test_question.question_text,
            "answers": json.loads(test_question.question_answers)
        }
        return render(request, './testing.html', obj)


def get_next_question(test_id, question_number):
    max_question = Testquestion.objects.filter(test_id=test_id).aggregate(Max('question_id'))
    if question_number <= max_question["question_id__max"]:
        next_question = Testquestion.objects.get(test_id=test_id, question_id=question_number)
        obj = {
            "testID": test_id,
            "number": next_question.question_id,
            "question": next_question.question_text,
            "answers": json.loads(next_question.question_answers)
        }
    else:
        obj = {"finish": "true"}
    return obj


def success_page(request):
    return render(request, './successpage.html')


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

    if answers and test_id and question_number:
        response_data = get_next_question(test_id, question_number + 1)
    elif test_id and question_number:
        response_data = get_next_question(test_id, question_number)
    else:
        pass

    return HttpResponse(json.dumps(response_data), content_type="application/json")
