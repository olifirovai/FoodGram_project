def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key.strip("nameIngredient_")
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value_ingredient
                ]
    return ingredients
