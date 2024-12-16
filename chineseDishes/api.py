from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from chineseDishes.models import Province, Dish, Ingridient, Dish_Ingridient
from chineseDishes.serializer import ProvinceSerializer, DishListSerializer, DishCreateSerializer, IngridientSerializer, Dish_IngridientListSerializer, Dish_IngridientCreateSerializer

class ProvincesViewSet(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class DishesViewSet(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Dish.objects.all()

    def get_serializer_class(self):
        if(self.action=='list'):
            return DishListSerializer
        else:
            return DishCreateSerializer
        
    def get_queryset(self):
        qs = super().get_queryset()

        if (self.request.user.is_superuser!=True):
            qs = qs.filter(user=self.request.user)

        return qs

class IngridientsViewSet(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer


class Dish_IngridientsViewSet(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Dish_Ingridient.objects.all()

    def get_serializer_class(self):
        if(self.action=='list'):
            return Dish_IngridientListSerializer
        else:
            return Dish_IngridientCreateSerializer
        
    def get_queryset(self):
        qs = super().get_queryset()

        if (self.request.user.is_superuser!=True):
            qs = qs.filter(user=self.request.user)

        return qs