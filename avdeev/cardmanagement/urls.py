from django.urls import include, re_path, path
from . import views

urlpatterns = [
    path('cardmanagement/', views.first_page_cards),
    path('cardgenerator/', views.page_card_generator),
    path('cardgenerator/checkseries/', views.check_card_series),
    path('cardgenerator/generate/', views.generate_cards),
    path('cardmanagement/updatefilter/', views.update_filter),
    path('cardmanagement/cardhistory/', views.card_history),
    path('cardmanagement/disablechacked/', views.disable_checked_card),
    path('cardmanagement/enablechacked/', views.enable_checked_card),
    path('cardmanagement/checkexpired/<int:action>/', views.check_expired_card),
]
