from math import floor

from django import template

register = template.Library()

@register.filter(name="convert_play")
def convert_play(value):
    hours = floor(value / 3600)
    minutes = floor((value - hours * 3600) / 60)
    seconds = value - hours * 3600 - minutes * 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


@register.filter(name="declension_of_product")
def declension_of_product(count):
    sufix = ("товар", "товара", "товаров")
    keys = (2, 0, 1, 1, 1, 2)
    mod = count % 100
    if 8 < mod < 20:
        sufix_key = 2
    else:
        sufix_key = keys[min(mod % 10, 5)]
    return sufix[sufix_key]
