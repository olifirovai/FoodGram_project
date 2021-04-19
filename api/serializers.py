from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipe.models import (Recipe, RecipeType)
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


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name', 'author', 'type', 'ingredients', 'directions',
            'cook_time',)
        model = Recipe


class RecipeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'type_name', 'color',)
        model = RecipeType
