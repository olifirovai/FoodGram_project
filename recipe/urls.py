from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_recipe/', views.recipe_create, name='create_recipe'),
    path('ingredients', views.get_ingredients_js, name='ingredients'),
    path('favorite_page/', views.favorite_recipes, name='favorite_recipes'),
    path('favorites', views.add_favorite_recipe, name='add_favorite_recipe'),
    path('favorites/<int:id>', views.remove_favorite_recipe,
         name='remove_favorite_recipe'),
    path('my_shopping_list/', views.shopping_list, name='my_shopping_list'),
    path('my_shopping_list/dowload/', views.dowload_shopping_list,
         name='dowload_shopping_list'),
    path('purchases', views.add_to_shopping_list, name='add_purchase'),
    path('purchases/<int:id>', views.remove_from_shopping_list,
         name='remove_purchase'),

    path('<username>/<slug:slug>/', views.recipe_view, name='recipe'),
    path('<username>/<slug:slug>/delete/', views.recipe_delete,
         name='delete_recipe'),
    path('<username>/<slug:slug>/edit/', views.recipe_edit,
         name='edit_recipe'),
]
