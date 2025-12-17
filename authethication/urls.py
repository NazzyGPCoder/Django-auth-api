from django.urls import path
from . import views
# from .views import register_user

urlpatterns = [
    
    # Auth endpoints
    path('register/', views.register_user, name='register'),
    path('login/',views.login_user, name='login')
    # path('login/', views.login_user, name='login'),
]