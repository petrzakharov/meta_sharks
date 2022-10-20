import datetime

from django.core.exceptions import ValidationError


def validate_past_order_date(value):
    if datetime.date.today() > value:
        raise ValidationError('Дата заказа не должна быть из прошлого')
    return value
