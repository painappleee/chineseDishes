from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
                "username": user.username
            })
        return Response(data)