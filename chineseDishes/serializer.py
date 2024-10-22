from rest_framework import serializers

from chineseDishes.models import Province, Dish, Ingridient, Dish_Ingridient

class ProvinceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Province
        fields = "__all__"

class DishListSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)

    class Meta:
        model = Dish
        fields = "__all__"

class DishCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = "__all__"

class IngridientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingridient
        fields = "__all__"

class Dish_IngridientListSerializer(serializers.ModelSerializer):
    dish = DishListSerializer(read_only=True)
    ingridient = IngridientSerializer(read_only=True)

    class Meta:
        model = Dish_Ingridient
        fields = "__all__"

class Dish_IngridientCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish_Ingridient
        fields = "__all__"