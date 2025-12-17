from django.urls import path
from . import views
from authentication.views import UserRoleUpdateView

urlpatterns = [
    path('users/<int:id>/role/', UserRoleUpdateView.as_view(), name='user-role-update'),
    # Auth endpoints
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('current/user',views.current_user,name="users info"),
    path('updated/user',views.update_user,name="update"),
]