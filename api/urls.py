from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import (RecipeViewSet, RecipeTypeReadOnlyViewSet, )

router = DefaultRouter()

router.register('recipes', RecipeViewSet, 'recipes')
router.register('types', RecipeTypeReadOnlyViewSet, 'types')

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),

]
