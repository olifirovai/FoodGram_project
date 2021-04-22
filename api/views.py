from rest_framework import permissions  # noqa
from rest_framework import viewsets

from recipe.models import (Recipe, RecipeType, )
from .serializers import (RecipeSerializer, RecipeTypeSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeTypeReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecipeTypeSerializer
    queryset = RecipeType.objects.all()

    # def get_queryset(self):
    #     types = get_object_or_404(Review, pk=self.kwargs['review_id'],
    #                                title__id=self.kwargs['title_id'])
    #     queryset = Recipe.objects.get_index_in_types(types)
    #     return queryset
