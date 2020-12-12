from .models import RecipeType


def get_url_with_types(request):
    url_type_line = f'{request.GET.urlencode()}&'
    return url_type_line


def get_filter_type(request):
    exclude_types = request.GET.getlist('type_exclude')
    types = RecipeType.objects.exclude(type_name__in=exclude_types)
    return types


def get_types(data):
    types_list = []

    for key in data:
        if data[key] == 'on':
            types_list.append(key)
    return types_list


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
