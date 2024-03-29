from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Ingredient
from .models import (Recipe, RecipeIngredient, FavoriteRecipe, ShoppingList,
                     RecipeType, RecipeTypeMapping, )


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient
        skip_unchanged = True
        fields = ('id', 'name', 'measure',)


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    resource_class = IngredientResource
    list_display = ('id', 'name', 'measure')
    search_fields = ('name', 'measure',)
    list_filter = ('name', 'measure',)
    empty_value_display = '-empty-'


class RecipeIngredientInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 2


class RecipeTypeInLine(admin.TabularInline):
    model = Recipe.type.through
    extra = 2


@admin.register(Recipe)
class RecipeAdmin(ImportExportModelAdmin):
    inlines = (RecipeIngredientInLine, RecipeTypeInLine)
    list_display = ['name', 'author', 'post_date']
    list_display_links = ['name']
    search_fields = ('name', 'post_date')
    empty_value_display = '-empty-'


@admin.register(RecipeTypeMapping)
class RecipeTypeMappingAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'type')
    search_fields = ('recipe', 'type')
    list_filter = ('recipe', 'type')
    empty_value_display = '-empty-'


@admin.register(RecipeType)
class RecipeTypeAdmin(admin.ModelAdmin):
    list_display = ('color', 'type_name')
    search_fields = ('color', 'type_name')
    list_filter = ('color', 'type_name')
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


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    search_fields = ('recipe', 'user',)
    list_filter = ('recipe', 'user',)
    empty_value_display = '-empty-'
