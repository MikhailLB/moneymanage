import requests
from celery import shared_task
from .models import Currency



@shared_task
def get_beat_currencies():
    curr = requests.get('https://api.exchangerate-api.com/v4/latest/USD').json()

    existing_currencies = {currency.code: currency for currency in Currency.objects.all()}

    for name, value in curr['rates'].items():
        if name in existing_currencies:
            curr_obj = existing_currencies[name]
            curr_obj.exchange_rate = value
            curr_obj.save()
        else:
            continue
    return "Successfully fetched currencies"
