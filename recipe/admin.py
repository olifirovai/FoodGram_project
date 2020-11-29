from django.contrib import admin

from .models import Recipe, RecipeIngredient, FavoriteRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'type', 'post_date')
    search_fields = ('name', 'post_date', 'type',)
    list_filter = ('name', 'post_date',)
    empty_value_display = '-empty-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'weight')
    search_fields = ('recipe', 'ingredient',)
    list_filter = ('recipe', 'ingredient',)
    empty_value_display = '-empty-'

@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    search_fields = ('user',)
    list_filter = ('recipe', 'user',)
    empty_value_display = '-empty-'