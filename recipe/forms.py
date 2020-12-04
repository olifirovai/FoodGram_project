from django.forms import ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'name', 'type', 'directions', 'cook_time', 'picture', 'ingredients'
        )
        labels = {'name': 'Recipe title', 'type': 'Recipe type',
                  'directions': 'Directions', 'ingredients': 'Ingredients',
                  'cook_time': 'Total cooking time', 'picture': 'Add an image'}

# class IngredientForm(ModelForm):
#     ingredient = forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=FRUIT_CHOICES))
#     class Meta:
#         model = RecipeIngredient
#         fields = ('ingredient', 'weight')
#         labels = {'ingredient': 'Ingredients', 'weight': 'Weight'}
