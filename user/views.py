import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.http import (require_http_methods,
                                          require_POST, )
from django.views.generic import CreateView

from foodgram.settings import OBJECT_PER_PAGE
from recipe.models import RecipeType, Recipe
from recipe.utils import (get_filter_type, get_url_with_types, )
from .forms import CreationForm
from .models import User, Follow


class SignUpView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'user/signup.html'


def user_profile(request, username):
    author = get_object_or_404(User, username=username)
    given_types = get_filter_type(request)
    recipe_list = Recipe.objects.get_author_recipes_in_types(author,
                                                             given_types)
    url_type_line = get_url_with_types(request)
    all_types = RecipeType.objects.all()
    paginator = Paginator(recipe_list, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {'author': author, 'paginator': paginator,
            'page': page, 'recipes': recipe_list, 'types': all_types,
            'given_types': given_types, 'url_type_line': url_type_line}
    return render(request, 'user/author_page.html', data)


@login_required
def follow_page(request):
    follow_list = Follow.objects.get_follow_list(request.user)
    paginator = Paginator(follow_list, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {'page': page, 'paginator': paginator}
    return render(request, 'user/follow_page.html', data)


@login_required
@require_POST
def follow_author(request):
    author_id = int(json.loads(request.body).get('id'))
    author = get_object_or_404(User, pk=author_id)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    data = {'success': 'true'}
    return JsonResponse(data)


@login_required
@require_http_methods('DELETE')
def unfollow_author(request, id):
    author = get_object_or_404(User, id=id)
    data = {'success': 'true'}
    follow = Follow.objects.get_follow(author, request.user)
    if not follow:
        data['success'] = 'false'
    follow.delete()
    return JsonResponse(data)
