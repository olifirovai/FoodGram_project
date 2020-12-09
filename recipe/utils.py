from .models import Recipe


def index_filter_tag(request):
    types = request.GET.get('type', 'breakfast,lunch,dinner,')
    url_type_line = types
    types = types[:-1].split(',')
    recipe_list = Recipe.objects.get_index_in_types(types)
    return recipe_list, types, url_type_line


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
    print(f'types_list={types_list} in get_types')
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
