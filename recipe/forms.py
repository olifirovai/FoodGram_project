from django.forms import ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'name', 'directions', 'cook_time', 'picture'
        )
        labels = {
            'name': 'Recipe title',
            'directions': 'Directions', 'cook_time': 'Total cooking time',
            'picture': 'Add an image'
        }
