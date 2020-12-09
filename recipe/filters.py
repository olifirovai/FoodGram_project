
from recipe.models import Recipe


import django_filters

class ProductFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Recipe
        fields = ['price', 'release_date']