from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_recipe/', views.recipe_create, name='create_recipe'),
    path('favorites/', views.favorite_recipes, name='favorite_recipes'),
    path('<username>/<slug:slug>/', views.recipe_view, name='recipe'),
    path('<username>/<slug:slug>/delete/', views.recipe_delete,
         name='delete_recipe'),
    path('<username>/<slug:slug>/edit/', views.recipe_edit,
         name='edit_recipe'),
]
