import requests
from celery import shared_task
from .models import Currency
from .currency_names import currency_names


@shared_task
def get_beat_currencies():
    curr = requests.get('https://api.exchangerate-api.com/v4/latest/USD').json()

    existing_currencies = {currency.code: currency for currency in Currency.objects.all()}

    for code, value in curr['rates'].items():
        if code in existing_currencies:
            curr_obj = existing_currencies[code]
            curr_obj.exchange_rate = value
            try:
                name = currency_names[code]
                curr_obj.name = name
            except:
                pass
            curr_obj.save()
        else:
            try:
                name = currency_names[code]
                Currency.objects.create(code=code, name=name, exchange_rate=value)
            except:
                pass

    return "Successfully fetched currencies"
