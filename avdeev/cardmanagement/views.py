from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date
import calendar
from .models import CardHistoryUse, CardBaseTable, StatusCard, OperationCard

import json


# Create your views here.
def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    hour = sourcedate.hour
    minute = sourcedate.minute
    return datetime(year, month, day, hour, minute)


def first_page_cards(request):
    return render(request, './index_cards.html')


def page_card_generator(request):
    return render(request, './card_generation.html')


def check_card_series(request):
    series = json.loads(request.body.decode('utf-8'))['series']
    if CardBaseTable.objects.filter(card_series=series).exists():
        exist="true"
    else:
        exist="false"
    response_data = {
        "series-exist": exist
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def generate_cards(request):
    new_card_count = 1
    form_data = json.loads(request.body.decode('utf-8'))
    card_series = int(form_data["card-series"])
    card_count = int(form_data["card-count"])
    card_create_date = datetime.strptime(form_data["card-create-date"], '%Y-%m-%dT%H:%M')
    optionsRadios = int(form_data["optionsRadios"])
    card_end_date = add_months(card_create_date, optionsRadios)
    card_amount = int(form_data["card-amount"])
    if datetime.now() >= card_create_date:
        status = StatusCard.objects.get(pk=1)
    else:
        status = StatusCard.objects.get(pk=2)
    for i in range(1, card_count + 1):
        new_card = CardBaseTable(card_series=card_series,
                                 card_number=new_card_count,
                                 card_create_date=card_create_date,
                                 card_end_date=card_end_date,
                                 card_last_use=card_create_date,
                                 card_amount=card_amount,
                                 card_status=status)
        new_card.save()
        new_card_count += 1
        card_operation=OperationCard.objects.get(pk=1)
        new_card_history_amount = CardHistoryUse(card_id=new_card,
                                                 card_operation=card_operation,
                                                 card_operation_detail=card_amount)
        new_card_history_amount.save()
        if datetime.now() >= card_create_date:
            card_operation = OperationCard.objects.get(pk=3)
            new_card_history_activate = CardHistoryUse(card_id=new_card,
                                                     card_operation=card_operation,
                                                     card_operation_detail=card_create_date)
            new_card_history_activate.save()
    all_new_cards = CardBaseTable.objects.filter(card_series=card_series)
    response_with_new_cards = []
    for item in all_new_cards:
        response_with_new_cards.append(
            {
                "card-series": item.card_series,
                "card-number": item.card_number,
                "card-create-date": item.card_create_date.strftime("%Y-%m-%d %H:%M"),
                "card-end-date": item.card_end_date.strftime("%Y-%m-%d %H:%M"),
                "card-last-use": item.card_last_use.strftime("%Y-%m-%d %H:%M"),
                "card-amount": item.card_amount,
                "card-status": item.card_status.Status_name
            }
        )
    return HttpResponse(json.dumps(response_with_new_cards), content_type="application/json")
