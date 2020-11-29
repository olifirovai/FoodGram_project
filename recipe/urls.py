from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_recipe/', views.recipe_create, name='create_recipe'),
    path('favorites/', views.favorite_recipes, name='favorite_recipes'),
    path('<username>/<slug:slug>/', views.recipe_view, name='recipe'),
]
