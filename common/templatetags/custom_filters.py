from django import template

register = template.Library()

@register.filter
def split_level(value):
    return value.split('-')

register.filter("split_level", split_level)

@register.filter
def filter_by_field_value(queryset, args):
    if args is None:
        return False
    arg_list = [arg.strip() for arg in args.split(',')]
    kwargs = {}
    for arg in arg_list:
        field, value = arg.split('=')
        kwargs[field.strip()] = value.strip()
    return queryset.filter(**kwargs)

def replace(value, args):
    if args is None:
            return False
    arg_list = [arg for arg in args.split(',')]    
    return value.replace(arg_list[0], arg_list[1])
