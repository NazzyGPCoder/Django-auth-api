from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from . import permissions
from .models import Restaurant, Categories, SubCategories, FoodItem
from .serializers import (
    RestaurantSerializer,
    CategoriesSerializer,
    SubCategoriesSerializer,
    FoodItemSerializer
)

from role.models import UserRole
from rest_framework.permissions import BasePermission

# -------------------------------------------------
# RESTAURANT VIEWS
# -------------------------------------------------

class RestaurantListCreateView(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAdminOrSuperAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.role == UserRole.SUPER_ADMIN:
            return Restaurant.objects.all()

        return Restaurant.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAdminOrSuperAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.role == UserRole.SUPER_ADMIN:
            return Restaurant.objects.all()

        return Restaurant.objects.filter(owner=user)
    
# -------------------------------------------------
# CATEGORY VIEWS
# -------------------------------------------------

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [permissions.IsReadOnlyOrAdmin]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [permissions.IsReadOnlyOrAdmin]



# -------------------------------------------------
# SUBCATEGORY VIEWS
# -------------------------------------------------

class SubCategoryListCreateView(generics.ListCreateAPIView):
    queryset = SubCategories.objects.all()
    serializer_class = SubCategoriesSerializer
    permission_classes = [permissions.IsReadOnlyOrAdmin]


class SubCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategories.objects.all()
    serializer_class = SubCategoriesSerializer
    permission_classes = [permissions.IsReadOnlyOrAdmin]


# -------------------------------------------------
# FOOD ITEM VIEWS
# -------------------------------------------------

class FoodItemListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.IsReadOnlyOrAdmin]

    def get_queryset(self):
        user = self.request.user

        # Anyone can view food items
        if self.request.method == 'GET':
            return FoodItem.objects.all()

        # Super Admin → all food items
        if user.role == UserRole.SUPER_ADMIN:
            return FoodItem.objects.all()

        # Admin → only their restaurant food items
        return FoodItem.objects.filter(restaurant__owner=user)


class FoodItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.IsReadOnlyOrAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.role == UserRole.SUPER_ADMIN:
            return FoodItem.objects.all()

        return FoodItem.objects.filter(restaurant__owner=user)
