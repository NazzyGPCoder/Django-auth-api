from django.urls import path
from .views import (
    RestaurantListCreateView, RestaurantDetailView,
    CategoryListCreateView, CategoryDetailView,
    SubCategoryListCreateView, SubCategoryDetailView,
    FoodItemListCreateView, FoodItemDetailView
)

urlpatterns = [
    # Restaurants
    path('restaurants/', RestaurantListCreateView.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),

    # Categories
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # SubCategories
    path('subcategories/', SubCategoryListCreateView.as_view(), name='subcategory-list'),
    path('subcategories/<int:pk>/', SubCategoryDetailView.as_view(), name='subcategory-detail'),

    # Food Items
    path('fooditems/', FoodItemListCreateView.as_view(), name='fooditem-list'),
    path('fooditems/<int:pk>/', FoodItemDetailView.as_view(), name='fooditem-detail'),
]
