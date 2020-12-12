import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.views.decorators.http import (require_http_methods,
                                          require_POST, )
from xhtml2pdf import pisa

from foodgram.settings import OBJECT_PER_PAGE
from user.models import User
from .forms import RecipeForm
from .models import (Recipe, ShoppingList, FavoriteRecipe, RecipeIngredient,
                     RecipeType, RecipeTypeMapping, Ingredient, )
from .utils import (get_ingredients, get_types, get_filter_type,
                    favorite_filter_tag, get_url_with_types, )

def get_recipe_list_by_type(types, *args, **kwargs):

    pass

def get_ingredients_js(request):
    text = request.GET.get('query')
    data = []
    ingredients = Ingredient.objects.filter(name__icontains=text).all()
    for ingredient in ingredients:
        data.append(
            {'title': ingredient.name, 'dimension': ingredient.measure})
    return JsonResponse(data, safe=False)


def index(request):
    given_types = get_filter_type(request)
    recipe_list = Recipe.objects.get_index_in_types(given_types)
    url_type_line = get_url_with_types(request, given_types)
    types = RecipeType.objects.all()
    paginator = Paginator(recipe_list, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {'paginator': paginator, 'page': page, 'types': types,
            'given_types': given_types, 'url_type_line': url_type_line}
    return render(request, 'index.html', data)


def recipe_view(request, username, slug):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(author.recipes, slug=slug)
    data = {'author': author, 'recipe': recipe}
    return render(request, 'recipe/recipe_page.html', data)


@login_required
def recipe_create(request):
    types = RecipeType.objects.all()
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        ingredients = get_ingredients(request.POST)
        recipe_types = get_types(request.POST)

        if form.is_valid():
            # TODO Здесь и в функции ниже - очень похожий код, который не очень
            # связан с вьюхой, но содержит в себе логику. При этом, логику
            # достаточно сложную. Лучше вынести в отдельные функции в модуль
            # утилзов и переиспользовать
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for type in recipe_types:
                recipe_type = RecipeTypeMapping(
                    recipe=recipe, type=RecipeType.objects.get(type_name=type)
                )
                recipe_type.save()

            for item in ingredients:
                recipe_ing = RecipeIngredient(
                    weight=item.get('weight'), recipe=recipe,
                    ingredient=Ingredient.objects.get(name=item.get('name'))

                )
                recipe_ing.save()

            form.save_m2m()
            return redirect('recipe', username=request.user.username,
                            slug=recipe.slug)

    else:
        form = RecipeForm()
    data = {'form': form, 'types': types}
    return render(request, 'recipe/recipe_form.html', data)


# TODO не работает сохранение картинки при редактировании рецепта
@login_required
def recipe_edit(request, username, slug):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(author.recipes, slug=slug)
    current_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    current_types = RecipeTypeMapping.objects.filter(recipe=recipe)
    types = RecipeType.objects.all()
    if request.user == author:
        form = RecipeForm(request.POST or None, files=request.FILES or None,
                          instance=recipe)

        if request.method == 'POST':
            if form.is_valid():
                recipe = form.save(commit=False)
                recipe_types = get_types(request.POST)
                ingredients = get_ingredients(request.POST)
                current_types.delete()
                current_ingredients.delete()

                for type in recipe_types:
                    recipe_type = RecipeTypeMapping(
                        recipe=recipe,
                        type=RecipeType.objects.get(type_name=type)
                    )
                    recipe_type.save()

                for item in ingredients:
                    recipe_ing = RecipeIngredient(
                        weight=item.get('weight'), recipe=recipe,
                        ingredient=Ingredient.objects.get(
                            name=item.get('name'))

                    )
                    recipe_ing.save()

                form.save_m2m()
                return redirect('recipe', username=recipe.author,
                                slug=recipe.slug)

        else:
            form = RecipeForm(instance=recipe)
        data = {'form': form, 'edit': True, 'author': author, 'recipe': recipe,
                'types': types}
        return render(request, 'recipe/recipe_form.html', data)

    else:
        return redirect('recipe', username=author, slug=recipe.slug)


@login_required
def recipe_delete(request, username, slug):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(author.recipes, slug=slug)
    if request.user == author:
        if request.method == 'POST':
            recipe.delete()
            return redirect('user_profile', username=username)
        data = {'author': author, 'recipe': recipe}
        return render(request, 'recipe/recipe_delete.html', data)


@login_required
def favorite_recipes(request):
    recipe_list, given_types, url_type_line = favorite_filter_tag(request)
    types = RecipeType.objects.all()
    paginator = Paginator(recipe_list, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {'page': page, 'paginator': paginator, 'types': types,
            'given_types': given_types, 'url_type_line': url_type_line}
    return render(request, 'recipe/favorite.html', data)


@login_required
@require_POST
def add_favorite_recipe(request):
    recipe_id = int(json.loads(request.body).get('id'))
    recipe = get_object_or_404(Recipe, id=recipe_id)
    FavoriteRecipe.objects.get_or_create(user=request.user, recipe=recipe)
    data = {'success': 'true'}
    return JsonResponse(data)


@login_required
@require_http_methods('DELETE')
def remove_favorite_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    FavoriteRecipe.objects.filter(user=request.user, recipe=recipe).delete()
    # TODO здесь должна быть не строка в ответе, а булевский True
    # True вижу, но по доке должен быть еще и False.
    # А вот его не вижу
    # Ниже аналогично
    data = {'success': 'true'}
    return JsonResponse(data)


@login_required
def shopping_list(request):
    shopping_list = ShoppingList.objects.get_shopping_list(request.user)
    data = {'shopping_list': shopping_list}
    return render(request, 'recipe/shopping_list.html', data)


@login_required
@require_POST
def add_to_shopping_list(request):
    recipe_id = int(json.loads(request.body).get('id'))
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
    data = {'success': 'true'}
    return JsonResponse(data)


@login_required
@require_http_methods('DELETE')
def remove_from_shopping_list(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    recipe_in_list = ShoppingList.objects.get(user=request.user, recipe=recipe)
    data = {'success': 'true'}
    if not recipe_in_list:
        data['success'] = 'false'
    recipe_in_list.delete()
    return JsonResponse(data)


@login_required
def dowload_shopping_list(request):
    cursor = connection.cursor()
    user = get_object_or_404(User, id=request.user.id)
    sql_string = f'SELECT * FROM total_weights WHERE user_id = {user.id}'
    # TODO Прямые запросы в базу это адекватно, если запрос слишком сложный,
    # чтобы сделать его с помощью ORM. Но это явно не наш случай.
    # Более того, это, опять же, очень сложная логика для вьюхи.
    # Генерацию файла лучше выделить в отдельную функцию, а здесь ее вызвать,
    # передав набор данных, нужный для рендера в файл

    cursor.execute(sql_string)
    ingredients_list = cursor.fetchall()
    # тут я пыталась сделать красиво=(
    template_path = 'recipe/shopping_template.html'
    # это простая версия PDF
    # template_path = 'recipe/pdf_template.html'
    context = {'ingredients': ingredients_list}
    response = HttpResponse(content_type='application/pdf')
    response[
        'Content-Disposition'] = 'attachment; filename="my_shopping_list.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='UTF-8')
    return response


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
