from rest_framework import serializers
from .models import Restaurant, Categories, SubCategories, FoodItem
from django.conf import settings


User = settings.AUTH_USER_MODEL

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = [
            'id',
            'name',
            'description',
            'price',
            'image',
            'available',
            'restaurant',
            'categories',
            'created_at'
        ]



class SubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategories
        fields = [
            'id',
            'name',
            'categories'
        ]


class CategoriesSerializer(serializers.ModelSerializer):
    subcategories = SubCategoriesSerializer(many=True, read_only=True)
    fooditems = FoodItemSerializer(many=True, read_only=True)

    class Meta:
        model = Categories
        fields = [
            'id',
            'name',
            'restaurant',
            'subcategories',
            'fooditems'
        ]



class RestaurantSerializer(serializers.ModelSerializer):
    categories = CategoriesSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField()  \

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'owner',
            'description',
            'address',
            'phonenumber',
            'image',
            'created_at',
            'categories'
        ]
