from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipe.models import (Recipe, RecipeType, Ingredient, RecipeIngredient)
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        default=email)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class RecipeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'type_name', 'color',)
        model = RecipeType


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measure',)
        model = Ingredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    recipe = serializers.SlugRelatedField(slug_field='name', read_only=True)
    ingredient = serializers.SlugRelatedField(slug_field='name', many=True,
                                              read_only=True)

    class Meta:
        fields = ('recipe', 'ingredient', 'weight',)
        model = RecipeIngredient


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    type = serializers.SlugRelatedField(many=True, slug_field='type_name',
                                        read_only=True)
    ingredients = serializers.SlugRelatedField(many=True, slug_field='name',
                                               read_only=True)

    class Meta:
        fields = ('id', 'name', 'author', 'type', 'ingredients', 'directions',
                  'cook_time',)
        model = Recipe
