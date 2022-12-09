from django.urls import include, re_path, path
from . import views

urlpatterns = [
    path('cardmanagement/', views.first_page_cards),
    path('cardgenerator/', views.page_card_generator),
    path('cardgenerator/checkseries/', views.check_card_series),
    path('cardgenerator/generate/', views.generate_cards),
]
