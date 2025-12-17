from django.contrib.auth import get_user_model, authenticate
from rest_framework import status,generics
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializer import CustomUserSerializer, UserRegistrationSerializer, UserUpdateSerializer,UserRoleUpdateSerializer
from core import permissions
User = get_user_model()


# ----------------------------------------
# Register a new user
# ----------------------------------------
@swagger_auto_schema(
    method='post',
    request_body=UserRegistrationSerializer,
    responses={201: CustomUserSerializer}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    return Response({
        'user': CustomUserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


# ----------------------------------------
# Login user and get JWT
# ----------------------------------------
login_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={  
        'email': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=['email', 'password']
)

@swagger_auto_schema(method='post', request_body=login_schema, responses={200: CustomUserSerializer})
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    
    if not user:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'user': CustomUserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


# ----------------------------------------
# Get current logged-in user
# ----------------------------------------
@swagger_auto_schema(method='get', responses={200: CustomUserSerializer})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Returns the currently logged-in user's info using JWT token.
    """
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ----------------------------------------
# Update current logged-in user
# ----------------------------------------
@swagger_auto_schema(method='put', request_body=UserUpdateSerializer, responses={200: CustomUserSerializer})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_user(request):
    """
    Update current user's info using JWT token.
    """
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(CustomUserSerializer(request.user).data, status=status.HTTP_200_OK)


# ----------------------------------------
# List all users (admin) or current user (normal)
# ----------------------------------------
@swagger_auto_schema(method='get', responses={200: CustomUserSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_users(request):
    """
    Admin: Fetch all users
    Normal user: Fetch only themselves
    """
    if request.user.is_staff:
        users = User.objects.all()
    else:
        users = User.objects.filter(id=request.user.id)  # Only current user

    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# users/views.py
class UserRoleUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRoleUpdateSerializer
    permission_classes = [permissions.IsAdminOrSuperAdmin]  # anyone logged in

    lookup_field = 'id'  # use /users/<id>/role/
