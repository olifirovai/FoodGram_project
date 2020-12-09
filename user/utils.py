from recipe.models import Recipe

def author_filter_tag(request):
    types = request.GET.get('type', 'breakfast,lunch,dinner,')
    url_type_line = types
    types = types[:-1].split(',')
    """Oh MY God!"""
    recipe_list = Recipe.objects.filter(author=request.user).all().filter(recipe_type__type__type_name__in=types).distinct()
    return recipe_list, types, url_type_line