from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .forms import RecipeForm
from .models import Recipe, RecipeIngredient, FavoriteRecipe


class RecipeAdminList(ChangeList):
    def __init__(self, request, model, list_display,
                 list_display_links, list_filter, date_hierarchy,
                 search_fields, list_select_related, list_per_page,
                 list_max_show_all, list_editable, model_admin, sorted_by):
        super(RecipeAdminList, self).__init__(request, model,
                                              list_display, list_display_links,
                                              list_filter,
                                              date_hierarchy, search_fields,
                                              list_select_related,
                                              list_per_page, list_max_show_all,
                                              list_editable,
                                              model_admin, sorted_by)

        self.list_display = ['name', 'author', 'post_date', 'type']
        self.list_display_links = ['name']
        self.search_fields = ('name', 'post_date', 'type',)
        self.empty_value_display = '-empty-'

class RecipeIngredientInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 3

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
