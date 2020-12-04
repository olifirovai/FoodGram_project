from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Ingredient


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

