from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime
import calendar
from .models import CardHistoryUse, CardBaseTable, StatusCard, OperationCard
from django.core.paginator import Paginator

import json


# Create your views here.

def get_parameters(params):
    if "card-series" not in params:
        params["card-series"] = ''
    if "card-number" not in params:
        params["card-number"] = ''
    if "card-create-date" not in params:
        params["card-create-date"] = ''
    if "card-end-date" not in params:
        params["card-end-date"] = ''
    if "card-amount" not in params:
        params["card-amount"] = ''
    if "card-last-use" not in params:
        params["card-last-use"] = ''
    if "card-status" not in params or params["card-status"] == "4":
        params["card-status"] = [1, 2, 3]
    else:
        lst_status = []
        lst_status.append(int(params["card-status"]))
        params["card-status"] = lst_status
    return params


def update_filter(request):
    params = get_parameters(json.loads(request.body.decode("utf-8")))
    print(params)
    all_cards = CardBaseTable.objects.filter(card_series__istartswith=f'{params["card-series"]}',
                                             card_number__istartswith=f'{params["card-number"]}',
                                             card_create_date__istartswith=f'{params["card-create-date"]}',
                                             card_end_date__istartswith=f'{params["card-end-date"]}',
                                             card_last_use__istartswith=f'{params["card-last-use"]}',
                                             card_status__in=params["card-status"],
                                             card_amount__istartswith=f'{params["card-amount"]}')
    response_data = serializers.serialize('json', all_cards)

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    hour = sourcedate.hour
    minute = sourcedate.minute
    return datetime(year, month, day, hour, minute)


def first_page_cards(request):
    filter_for_pagination = ''
    params = request.GET.copy()
    if "card-series" not in params:
        params["card-series"] = ''
    else:
        filter_for_pagination += f'&card-series={params["card-series"]}'

    if "card-number" not in params:
        params["card-number"] = ''
    else:
        filter_for_pagination += f'&card-number={params["card-number"]}'

    if "card-create-date" not in params:
        params["card-create-date"] = ''
    else:
        filter_for_pagination += f'&card-create-date={params["card-create-date"]}'

    if "card-end-date" not in params:
        params["card-end-date"] = ''
    else:
        filter_for_pagination += f'&card-end-date={params["card-end-date"]}'

    if "card-amount" not in params:
        params["card-amount"] = ''
    else:
        filter_for_pagination += f'&card-amount={params["card-amount"]}'

    if "card-last-use" not in params:
        params["card-last-use"] = ''
    else:
        filter_for_pagination += f'&card-last-use={params["card-last-use"]}'

    if "card-status" not in params or params["card-status"] == "4":
        params["card-status"] = [1, 2, 3]
        filter_for_pagination += f'&card-status=4'
    else:
        lst_status = []
        lst_status.append(int(params["card-status"]))
        filter_for_pagination += f'&card-status={int(params["card-status"])}'
        params["card-status"] = lst_status

    all_cards = CardBaseTable.objects.filter(card_series__istartswith=f'{params["card-series"]}',
                                             card_number__istartswith=f'{params["card-number"]}',
                                             card_create_date__istartswith=f'{params["card-create-date"]}',
                                             card_end_date__istartswith=f'{params["card-end-date"]}',
                                             card_last_use__istartswith=f'{params["card-last-use"]}',
                                             card_status__in=params["card-status"],
                                             card_amount__istartswith=f'{params["card-amount"]}')
    paginator = Paginator(all_cards, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, './index_cards.html', {'page_obj': page_obj,
                                                  'card_series': params["card-series"],
                                                  'card_number': params["card-number"],
                                                  "card_create_date": params["card-create-date"],
                                                  "card_end_date": params["card-end-date"],
                                                  "card_last_use": params["card-last-use"],
                                                  "card_amount": params["card-amount"],
                                                  "filter_for_pagination": filter_for_pagination})


def page_card_generator(request):
    return render(request, './card_generation.html')


def check_card_series(request):
    series = json.loads(request.body.decode('utf-8'))['series']
    if CardBaseTable.objects.filter(card_series=series).exists():
        exist = "true"
    else:
        exist = "false"
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
        card_operation = OperationCard.objects.get(pk=1)
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


def push_history_record(id, action, amount=0):
    new_history_record = CardHistoryUse()
    if action == 1:
        new_history_record.card_id = CardBaseTable.objects.get(pk=id)
        new_history_record.card_operation = OperationCard.objects.get(pk=1)
        new_history_record.card_operation_detail = amount
    if action == 2:
        new_history_record.card_id = CardBaseTable.objects.get(pk=id)
        new_history_record.card_operation = OperationCard.objects.get(pk=2)
        new_history_record.card_operation_detail = amount
    if action == 3:
        new_history_record.card_id = CardBaseTable.objects.get(pk=id)
        new_history_record.card_operation = OperationCard.objects.get(pk=3)
        new_history_record.card_operation_detail = datetime.now()
    if action == 4:
        new_history_record.card_id = CardBaseTable.objects.get(pk=id)
        new_history_record.card_operation = OperationCard.objects.get(pk=4)
        new_history_record.card_operation_detail = datetime.now()
    if action == 5:
        new_history_record.card_id = CardBaseTable.objects.get(pk=id)
        new_history_record.card_operation = OperationCard.objects.get(pk=5)
        new_history_record.card_operation_detail = datetime.now()

    new_history_record.save()


def check_expired_card(request, action=0):
    count = 0
    if action in [2, 3]:
        if action == 2:
            status = 3
        else:
            status = 1
        expcard = CardBaseTable.objects.filter(card_end_date__lt=datetime.now(), card_status=status)
        status = StatusCard.objects.get(pk=action)
        for card in expcard:
            card.card_status = status
            if action == 2: push_history_record(card.id, action)
            card.save()
            count += 1
        if action == 2:
            response_data = {
                "disable": f"Отключено {count} карт"
            }
        else:
            response_data = {
                "expired": f"Просрочено {count} карт"
            }
    else:
        response_data = {
            "Ошибка": f"запрос не распознан"
        }
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def update_use_date(id):
    card = CardBaseTable.objects.get(pk=id)
    card.card_last_use = datetime.now()
    card.save()

def disable_checked_card(request):
    list_card_to_didable = [int(i) for i in json.loads(request.body.decode("utf-8"))]
    cards_to_disable = CardBaseTable.objects.filter(pk__in=list_card_to_didable)
    for card in cards_to_disable:
        card.card_status = StatusCard.objects.get(pk=2)
        push_history_record(card.id, 4)
        card.save()
        update_use_date(card.id)
    print(len(cards_to_disable))
    response_data = {
        "отключили": list_card_to_didable
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def enable_checked_card(request):
    list_card_to_enable = [int(i) for i in json.loads(request.body.decode("utf-8"))]
    cards_to_enable = CardBaseTable.objects.filter(pk__in=list_card_to_enable)
    for card in cards_to_enable:
        card.card_status = StatusCard.objects.get(pk=1)
        push_history_record(card.id, 3)
        card.save()
        update_use_date(card.id)

    print(len(cards_to_enable))
    response_data = {
        "Включили": list_card_to_enable
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def card_history(request):
    obj = [int(n) for n in request.COOKIES['params'].split(',')]
    print('stop')
    all_cards = []
    for i in obj:
        history = CardHistoryUse.objects.filter(card_id_id=i).select_related('card_id')
        all_cards.append({"card": history})
    print('stop')
    print(all_cards)
    return render(request, './card_history.html', {'history': all_cards})


def check_balance_card(id):
    card = CardBaseTable.objects.get(pk=id)
    if card.card_amount==0:
        push_history_record(id,5)
        card.card_status = StatusCard.objects.get(pk=2)
        push_history_record(id, 4)
        card.save()
        update_use_date(card.id)

def account_movement(request):
    body = json.loads(request.body.decode("utf-8"))
    cards = [int(n) for n in body["cards"]]
    success_count = 0
    error_count = 0
    for card in cards:
        card = CardBaseTable.objects.get(pk=card)
        if card.card_status == StatusCard.objects.get(pk=1):
            if body['action'] == 'push':
                card.card_amount += int(body['amount'])
                card.save()
                update_use_date(card.id)
                push_history_record(card.id, 1, int(body['amount']))
                success_count += 1
            elif body['action'] == "pull":
                if card.card_amount < int(body['amount']):
                    error_count += 1
                else:
                    card.card_amount -= int(body['amount'])
                    push_history_record(card.id, 2, int(body['amount']))
                    success_count += 1
                card.save()
                update_use_date(card.id)
            check_balance_card(card.id)
        else:
            error_count += 1

    print(body)

    response_data = {
        "Успех": success_count,
        "Неудача": error_count
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")
