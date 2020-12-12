from .models import Recipe, RecipeType


def get_url_with_types(request, types):
    if types:
        url_type_line = f'{request.GET.urlencode()}&'

    else:
        url_type_line = ''
    print(types)
    return url_type_line


def collect_data_with_types():
    pass


def get_filter_type(request):
    types = request.GET.getlist('type_exclude')
    print(f'types={type(types)}')
    # types = RecipeType.objects
    print(types)

    return types


def favorite_filter_tag(request):
    types = request.GET.get('type', 'breakfast,lunch,dinner,')
    url_type_line = types
    types = types[:-1].split(',')
    recipe_list = Recipe.objects.get_favorite_in_types(request.user, types)
    return recipe_list, types, url_type_line


def get_types(data):
    types_list = []

    for key in data:
        if data[key] == 'on':
            types_list.append(key)
    print(types_list)
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
