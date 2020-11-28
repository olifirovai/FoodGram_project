from django.forms import ModelForm

from .models import Recipe, RecipeIngredient


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'type', 'directions', 'cook_time', 'picture')
        labels = {'name': 'Recipe title', 'type': 'Recipe type',
                  'directions': 'Directions',
                  'cook_time': 'Total cooking time', 'picture': 'Image'}


# class IngredientForm(ModelForm):
#     ingredient = forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=FRUIT_CHOICES))
#     class Meta:
#         model = RecipeIngredient
#         fields = ('ingredient', 'weight')
#         labels = {'ingredient': 'Ingredients', 'weight': 'Weight'}
