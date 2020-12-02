from django import template
from recipe.models import Recipe
register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg

@register.filter('recipe_type')
def filter_types(type):
    recipe_list = Recipe.objects.get_certain_type(type)
    return recipe_list



@register.filter('duration_format')
def duration_format(value):
    value = int(value)
    h = 'hour'
    m = 'minute'
    hours = int(value / 60)
    minutes = value % 60
    if hours > 1:
        h += 's'
    if minutes > 1:
        m += 's'

    if hours == 0:
        return f'{minutes} {m}'
    return f'{hours} {h}, {minutes} {m}'

