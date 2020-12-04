from django.contrib import admin

from .models import Recipe, RecipeIngredient, FavoriteRecipe


class RecipeIngredientInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInLine,)
    list_display = ['name', 'author', 'post_date', 'type']
    list_display_links = ['name']
    search_fields = ('name', 'post_date', 'type',)
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
