from rest_framework import serializers

from chineseDishes.models import Province, Dish, Ingridient, Dish_Ingridient
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ProvinceCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
            
        if (validated_data['picture']== None):
            validated_data['picture'] = "chineseDishes/noimage.png"

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if (validated_data['picture']== None):
            validated_data['picture'] = "chineseDishes/noimage.png"

        return super().update(instance, validated_data)

    class Meta:
        model = Province
        fields = "__all__"


class ProvinceListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Province
        fields = "__all__"


class DishListSerializer(serializers.ModelSerializer):
    province = ProvinceListSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Dish
        fields = "__all__"

class DishCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user

        if (validated_data['picture']== None):
            validated_data['picture'] = "chineseDishes/noimage.png"

        return super().create(validated_data)
    

    def update(self, instance, validated_data):
        if (validated_data['picture']== None):
            validated_data['picture'] = "chineseDishes/noimage.png"

        return super().update(instance, validated_data)
    

    class Meta:
        model = Dish
        fields = "__all__"

class IngridientListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Ingridient
        fields = "__all__"

class IngridientCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingridient
        fields = "__all__"

class Dish_IngridientListSerializer(serializers.ModelSerializer):
    dish = DishListSerializer(read_only=True)
    ingridient = IngridientListSerializer(read_only=True)

    class Meta:
        model = Dish_Ingridient
        fields = "__all__"

class Dish_IngridientCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user

        return super().create(validated_data)
     
    class Meta:
        model = Dish_Ingridient
        fields = "__all__"