import code

import value
from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
    'rub': 'руб',
    'usd': '$',
}


# Регистрируем фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблона, а не простая функция.

@register.filter()
def currency(value, code='rub'):
    """
    value: значение, к которому нужно применить фильтр

    """
    postfix = CURRENCIES_SYMBOLS[code]
    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value} {postfix}'
