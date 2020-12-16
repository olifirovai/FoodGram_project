from .models import RecipeType, RecipeTypeMapping, RecipeIngredient, Ingredient


def get_url_with_types(request):
    url_type_line = request.GET.get('type')
    return url_type_line


def get_filter_type(request):
    try:
        given_types = list(request.GET.get('type'))
    except:
        given_types = None
    return given_types


def get_types(data):
    types_list = []
    for key in data:
        if key != 'picture' and key != 'picture-clear':
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


def save_ingredients(recipe, ingredients):
    for item in ingredients:
        # он сохраняет вес рывный 0, но выдает ошибку если отрицательный
        # хотя когда создаю рецепт в админке, не пропускает ноль.
        # вообщем, промучившись, я сделала трюк, если будет ноль > конвертить
        # его в отрицательно число =(((
        if item.get('weight') == 0:
            item['weight'] = -5
        recipe_ing = RecipeIngredient.objects.create(
            weight=item.get('weight'), recipe=recipe,
            ingredient=Ingredient.objects.get(name=item.get('name'))

        )
        recipe_ing.save()


def save_types(recipe, types):
    for type in types:
        recipe_type = RecipeTypeMapping.objects.create(
            recipe=recipe, type=RecipeType.objects.get(type_name=type)
        )
        recipe_type.save()
