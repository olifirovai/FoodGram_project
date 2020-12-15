from django import template

from recipe.models import FavoriteRecipe, ShoppingList, RecipeTypeMapping

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter()
def is_in_type(type, recipe):
    type_exists = RecipeTypeMapping.objects.filter(type=type,
                                                   recipe=recipe).exists()
    return type_exists


@register.filter()
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


@register.filter()
def is_favorite(user, recipe):
    favorite = FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists()
    return favorite


@register.filter()
def is_in_shopping(user, recipe):
    in_shopping = ShoppingList.objects.filter(user=user,
                                              recipe=recipe).exists()
    return in_shopping


@register.filter()
def recipe_shopping_count(user):
    recipe_amount = ShoppingList.objects.get_shopping_list(user).count()
    return recipe_amount


@register.filter()
def ingredients(ingredients, i):
    return ingredients[i]


@register.filter()
def get_type_url(type_name):
    url_line = f'type_exclude={type_name}&'
    return url_line


@register.filter()
def add_type_to_url(url, type_name):
    url_line = f'type_exclude={type_name}&'
    return url + url_line


@register.filter
def url_with_get(request, number):
    query = request.GET.copy()
    query['page'] = number
    return query.urlencode()
