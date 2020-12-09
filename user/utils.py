from recipe.models import Recipe


def author_filter_tag(request, author):
    types = request.GET.get('type', 'breakfast,lunch,dinner,')
    url_type_line = types
    types = types[:-1].split(',')
    """Oh MY God!"""
    recipe_list = Recipe.objects.get_author_recipes_in_types(author, types)
    return recipe_list, types, url_type_line
