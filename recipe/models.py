import random
import string

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils.text import slugify

from user.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=5000, verbose_name='ingredient\'s name',
                            unique=True)
    measure = models.CharField(max_length=100, verbose_name='measurement unit')

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.measure})'


class RecipeType(models.Model):
    TYPE_CHOICES = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    )
    type_name = models.CharField(max_length=25, choices=TYPE_CHOICES,
                                 unique=True)
    color = models.CharField(max_length=10, default='', editable=False)

    class Meta:
        verbose_name = 'Recipe type'
        verbose_name_plural = 'Recipe types'
        ordering = ['type_name']

    def save(self, *args, **kwargs):
        if self.type_name == 'dinner':
            self.color = 'purple'
        elif self.type_name == 'lunch':
            self.color = 'green'
        else:
            self.color = 'orange'

        super(RecipeType, self).save(*args, **kwargs)

    def __str__(self):
        return self.type_name


class RecipeManager(models.Manager):

    def get_index_in_types(self, types):
        return self.get_queryset().filter(type__in=types).distinct()

    def get_author_recipes_in_types(self, author, types):
        return self.get_queryset().filter(author=author,
                                          type__in=types).distinct()

    def get_favorite_recipes(self, user):
        return self.get_queryset().filter(favorite_recipe__user=user)

    def get_favorite_in_types(self, user, types):
        return self.get_favorite_recipes(user).filter(
            type__in=types).distinct()


class Recipe(models.Model):
    name = models.CharField(max_length=200, verbose_name='recipe\'s name')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    type = models.ManyToManyField(RecipeType, through='RecipeTypeMapping')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient')
    directions = models.TextField()
    post_date = models.DateTimeField(auto_now=True, db_index=True,
                                     verbose_name='publishing date')
    cook_time = models.IntegerField(
        verbose_name='cook time', null=False,
        validators=[MinValueValidator(1)], default=10,
        help_text='Add cook time in minutes'
    )
    picture = models.ImageField(upload_to='recipe/',
                                verbose_name='picture of the recipe',
                                blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True)
    objects = RecipeManager()

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-post_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            random_mark = ''.join(
                random.choice(string.ascii_letters + string.digits) for _ in
                range(6)
            )
            self.slug = slugify(self.name + '-' + random_mark)
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.name[:30]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredient')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT,
                                   related_name='recipe_ingredient')
    weight = models.IntegerField(
        verbose_name='ingredient weight', null=False,
        validators=[MinValueValidator(1)], default=10,
        help_text='Add needed weight for the recipe'
    )

    class Meta:
        unique_together = ('recipe', 'ingredient')
        verbose_name = 'Recipe Ingredient'
        verbose_name_plural = 'Recipes Ingredients'
        ordering = ['recipe']


class RecipeTypeMapping(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_type')
    type = models.ForeignKey(RecipeType, on_delete=models.PROTECT,
                             related_name='recipe_type')

    class Meta:
        unique_together = ('recipe', 'type')
        verbose_name = 'Recipe type mapping'
        verbose_name_plural = 'Recipes types mapping'
        ordering = ['type']

    def __str__(self):
        return f'{self.recipe} has types: {self.type}'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='liker')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorite_recipe')

    class Meta:
        unique_together = ('recipe', 'user')
        verbose_name = 'Favorite Recipe'
        verbose_name_plural = 'Favorite Recipes'
        ordering = ['user']

    def __str__(self):
        return f'favorite recipe - {self.recipe.name}'


class ShoppingListManager(models.Manager):
    def get_shopping_list(self, user):
        return self.get_queryset().filter(user=user)

    def get_weights_in_shopping_list(self, user):
        users_recipe = self.get_shopping_list(user)
        print(users_recipe)
        recipe = [recipe.recipe for recipe in users_recipe]
        print(recipe)
        weights_list = RecipeIngredient.objects.filter(
            recipe__in=recipe
        ).values(
            'ingredient__name', 'ingredient__measure'
        ).annotate(
            Sum('weight')
        )
        return weights_list


class ShoppingList(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='shopping_list')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shopping_list')
    objects = ShoppingListManager()

    class Meta:
        unique_together = ('recipe', 'user')
        verbose_name = 'Shopping List'
        verbose_name_plural = 'Shopping Lists'
        ordering = ['recipe']

    def __str__(self):
        return f'shopping list for {self.recipe}'
