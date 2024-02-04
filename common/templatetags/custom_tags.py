from django import template
from common.models import MyCounter

register = template.Library()

@register.simple_tag
def my_custom_tag2(arg1, arg2):
    # عملیات‌های مورد نیاز
    return 2

@register.simple_tag
def calculate(value1=None, operator="", value2=None, name="default"):

    if isinstance(value1, str) or value1 is None:
        value = MyCounter.objects.filter(name=name).last().value
    else:
         value = value1

    if operator == "+":
        if value2 is None:
            value2 = 0
        MyCounter.objects.create(name=name, value=value + value2)
    elif operator == "-":
        if value2 is None:
            value2 = 0
        MyCounter.objects.create(name=name, value=value - value2)
    elif operator == "*":
        if value2 is None:
            value2 = 1
        MyCounter.objects.create(name=name, value=value * value2)
    elif operator == "/":
        if value2 is None:
            value2 = 1
        MyCounter.objects.create(name=name, value=value / value2)
    else:
        MyCounter.objects.create(name=name, value=value)
    return MyCounter.objects.filter(name=name).last().value


@register.simple_tag
def tag_by_field_value(queryset, *args):
    kwargs = {}
    for arg in args:
        field, value = arg.split('=')
        kwargs[field.strip()] = value.strip()
    return queryset.filter(**kwargs)