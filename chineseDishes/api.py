from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Max, Min

from chineseDishes.models import Province, Dish, Ingridient, Dish_Ingridient
from chineseDishes.serializer import ProvinceListSerializer, ProvinceCreateSerializer, DishListSerializer, DishCreateSerializer, IngridientListSerializer, IngridientCreateSerializer, Dish_IngridientListSerializer, Dish_IngridientCreateSerializer 

class ProvincesViewSet(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):

    queryset = Province.objects.all()

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        maxPop = serializers.IntegerField()
        minPop = serializers.IntegerField()
        maxArea = serializers.IntegerField()
        minArea = serializers.IntegerField()


    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Province.objects.aggregate(
            count = Count("*"),
            maxPop = Max("population"),
            minPop = Min("population"),
            maxArea = Max("area"),
            minArea = Min("area"),              
        )

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)
    
    def get_serializer_class(self):
        if(self.action=='list'):
            return ProvinceListSerializer
        else:
            return ProvinceCreateSerializer

class DishesViewSet(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):

    queryset = Dish.objects.all()

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        stats = Dish.objects.aggregate(
            count = Count("*"),
            avg = Avg("spice_level"),
            max = Max("spice_level"),
            min = Min("spice_level"),             
        )

        serializer = self.StatsSerializer(instance=stats)

        return Response(serializer.data)

    def get_serializer_class(self):
        if(self.action=='list'):
            return DishListSerializer
        else:
            return DishCreateSerializer
        
class IngridientsViewSet(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Ingridient.objects.all()

    def get_serializer_class(self):
        if(self.action=='list'):
            return IngridientListSerializer
        else:
            return IngridientCreateSerializer


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
    
class UserProfileViewSet(GenericViewSet):

    class LoginSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

    class RegisterSerializer(serializers.Serializer):
        username = serializers.CharField()
        email = serializers.EmailField()
        password = serializers.CharField()

    @action(url_path="login", detail=False, methods=["POST"])
    def login(self, request, *args, **kwargs):

        serializer = self.LoginSerializer(data=request.data)

        if (serializer.is_valid()):
            userdata = serializer.validated_data
            user = authenticate(username = userdata['username'], password=userdata['password'])

            if (user is not None):
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            else: 
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    @action(url_path="logout", detail=False, methods=["POST"])
    def logout(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)

    @action(url_path="register", detail=False, methods=["POST"])
    def register(self, request, *args, **kwargs):
        serializer = self.RegisterSerializer(data=request.data)

        if (serializer.is_valid()):
            userdata = serializer.validated_data

            try:
                user = User.objects.create_user(username=userdata['username'], email=userdata['email'], password=userdata['password'])
                user.save()
                user = authenticate(username = userdata['username'], password=userdata['password'])
                login(request, user)

                return Response(status=status.HTTP_200_OK)
            
            except: return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(url_path="info", detail=False, methods=["GET"])
    def get_user(self, request, *args, **kwargs):
        user = request.user
        data = {"is_authenticated": user.is_authenticated}
        if user.is_authenticated:
            data.update({
                "is_superuser": user.is_superuser,
                "username": user.username,
            })
        return Response(data)
    
class ресепти(GenericViewSet):
    @action(url_path="полутить", detail=False, methods=["GET"])
    def полутить(self, *args, **kwargs):
        return Response("всё так вкусно, давай лучше это скушаем!")
    
    @action(url_path="ктозопа", detail=False, methods=["GET"])
    def ктозопа(self, *args, **kwargs):
        return Response("ты не зопа )( 😊😊😊")
    
    @action(url_path="ктомаленьки", detail=False, methods=["GET"])
    def ктомаленьки(self, *args, **kwargs):
        return Response("я")
    
class RecipesViewSet(GenericViewSet):
    def get_queryset(self):
        return Dish.objects.all()
    
    @action(url_path="get", detail=False, methods=["GET"])
    def getRecipes(self, *args, **kwargs):
        dishes_all = Dish.objects.all()
        ingridients_all = Dish_Ingridient.objects.all()

        ingridients_by_dish = {}
        for ingridient in ingridients_all:
            ingridients_by_dish.setdefault(ingridient.dish_id, []).append({
                "id": ingridient.id,
                "ingridient": ingridient.ingridient.name,
                "quantity": ingridient.quantity,
                "typeQuantity": ingridient.typeQuantity
            })

        dishes_data = []
        for dish in dishes_all:
            dish_data = {
                "id": dish.id,
                "name": dish.name,
                "province": dish.province.name,
                "picture": dish.picture.url if dish.picture else None,
                "ingridients": ingridients_by_dish.get(dish.id, []),  # Список ингредиентов
            }
            dishes_data.append(dish_data)

        return Response(dishes_data)
        

    
