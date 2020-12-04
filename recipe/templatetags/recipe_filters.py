from django import template

from recipe.models import Recipe, FavoriteRecipe, ShoppingList

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
    elif minutes == 0:
        return f'{hours} {h}'
    return f'{hours} {h}, {minutes} {m}'


@register.filter(name='check_favorite')
def check_favorite(user, recipe):
    favorite = FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists()
    return favorite

@register.filter(name='check_in_shopping')
def check_in_shopping(user, recipe):
    in_shopping = ShoppingList.objects.filter(user=user, recipe=recipe).exists()
    return in_shopping


@register.filter(name='recipe_shopping_count')
def recipe_shopping_count(user):
    recipe_amount = ShoppingList.objects.get_shopping_list(user).count()
    return recipe_amount