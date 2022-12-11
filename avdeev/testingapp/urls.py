from django.urls import path
from . import views

urlpatterns = [
    # post views
    path('appfortests', views.first_page_tests),
    path('testing/<int:test_id>/', views.testing_page),
    path('getquestion/', views.get_question_response),
    path('test/logout/', views.logoutuser),
    path('statistics/', views.get_statistics),
    path('success/', views.success_page),
    path('login/', views.user_login, name='login'),
    path('registration/', views.user_register, name='registration'),
]