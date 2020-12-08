from django.core.paginator import Paginator
from django.db.models import Q

from .models import Recipe


def get_ingredients(data):
    ingredient_numbers = set()
    ingredients = []

    for key in data:
        if key.startswith('nameIngredient_'):
            _, number = key.split('_')
            ingredient_numbers.add(number)
    for number in ingredient_numbers:
        ingredients.append(
            {
                'name': data[f'nameIngredient_{number}'],
                'measure': data[f'unitsIngredient_{number}'],
                'weight': int(data[f'valueIngredient_{number}']),
            }
        )

    return ingredients


def filter_by_tags(request, view, user):
    filters = request.GET.getlist('filters')

    filters_by_views = {
        'index': Q(),
        'favourites': Q(favorited_recipe__user=request.user),
        'profile': Q(author=user),
    }

    recipe_list = Recipe.taged.filter_for_tags(
        filters).filter(filters_by_views[view]).distinct()

    paginator = Paginator(recipe_list, 9)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return paginator, page
