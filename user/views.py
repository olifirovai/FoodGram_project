from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm
from .models import User, Follow


class SignUpView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'user/signup.html'


def user_profile(request, username):
    author = get_object_or_404(User, username=username)
    recipe = author.recipes.filter(author=author)
    paginator = Paginator(recipe, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {'author': author, 'paginator': paginator,
            'page': page}
    return render(request, 'user/author_page.html', data)


def follow_page(request):
    follow_list = Follow.objects.get_follow_list(request.user)
    paginator = Paginator(follow_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    data = {'page': page, 'paginator': paginator}
    return render(request, 'user/follow_page.html', data)
