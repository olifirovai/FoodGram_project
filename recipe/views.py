

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import RecipeForm
from .models import Recipe
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from user.models import User


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


def recipe_create(request):
    if request.method == 'POST':
        form_recipe = RecipeForm(request.POST or None, files=request.FILES or None)
        if form_recipe.is_valid():
            recipe = form_recipe.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipe', username=request.user.username, slug=recipe.slug)
    else:
        form_recipe = RecipeForm()
    return render(request, 'recipe/create_recipe.html', {'form': form_recipe})


def recipe_edit():
    pass


def recipe_delete():
    pass

def favorite_recipes(request):
    recipe_list = Recipe.objects.get_favorite_recipes(request.user)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {'page': page, 'paginator': paginator}
    return render(request, 'recipe/favorite.html', data)

def recipe_type():
    pass

# def add_favorite_recipe(request, username, post_id):
#     author = get_object_or_404(User, username=username)
#     post = get_object_or_404(author.author_posts, id=post_id)
#     if request.user != author:
#         Like.objects.get_or_create(user=request.user, post=post)
#     return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
#
#
# def remove_favorite_recipe(request, username, post_id):
#     author = get_object_or_404(User, username=username)
#     post = get_object_or_404(author.author_posts, id=post_id)
#     Like.objects.filter(user=request.user, post=post).delete()
#     return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
