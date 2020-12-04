import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import (require_http_methods,
                                          require_POST, )

from user.models import User
from .forms import RecipeForm
from .models import Recipe, ShoppingList, FavoriteRecipe


def index(request):
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {'paginator': paginator, 'page': page}
    return render(request, 'index.html', data)


def recipe_view(request, username, slug):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(author.recipes, slug=slug)
    data = {'author': author, 'recipe': recipe}
    return render(request, 'recipe/recipe_page.html', data)


@login_required
def recipe_create(request):
    if request.method == 'POST':
        form_recipe = RecipeForm(request.POST or None,
                                 files=request.FILES or None)
        if form_recipe.is_valid():
            recipe = form_recipe.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipe', username=request.user.username,
                            slug=recipe.slug)
    else:
        form_recipe = RecipeForm()
    return render(request, 'recipe/recipe_form.html', {'form': form_recipe})


def recipe_edit(request, username, slug):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(author.recipes, slug=slug)
    if request.user == author:
        form = RecipeForm(request.POST or None, files=request.FILES or None,
                          instance=recipe)
        if request.method == 'POST':
            if form.is_valid():
                recipe = form.save()
                return redirect('recipe', username=recipe.author,
                                slug=recipe.slug)
        else:
            form = RecipeForm(instance=recipe)
        data = {'form': form, 'edit': True, 'author': author, 'recipe': recipe}
        return render(request, 'recipe/recipe_form.html', data)
    else:
        return redirect('recipe', username=author, slug=recipe.slug)


def recipe_delete(request, username, slug):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(author.recipes, slug=slug)
    if request.user == author:
        if request.method == 'POST':
            recipe.delete()
            return redirect('user_profile', username=username)
        data = {'author': author, 'recipe': recipe}
        return render(request, 'recipe/recipe_delete.html', data)


def recipe_type():
    pass


@login_required
def favorite_recipes(request):
    recipe_list = Recipe.objects.get_favorite_recipes(request.user)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {'page': page, 'paginator': paginator}
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


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)