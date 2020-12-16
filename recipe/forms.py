from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    picture = forms.ImageField(
        required=True,
        label='Add an image'
    )

    class Meta:
        model = Recipe
        fields = (
            'name', 'directions', 'cook_time', 'picture'
        )

        labels = {
            'name': 'Recipe title', 'cook_time': 'Total cooking time',
            'directions': 'Directions', 'picture': 'Add an image'
        }
