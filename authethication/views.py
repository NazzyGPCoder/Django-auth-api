from django.shortcuts import render
from .serializer import (
    CustomUserSerializer, UserRegistrationSerializer, UserLoginSerializer
)
from rest_framework.decorators import api_view, permission_classes,parser_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema




# Create your views here.


# @swagger_auto_schema(method='post', request_body=UserRegistrationSerializer, responses={201: CustomUserSerializer})
@swagger_auto_schema(
    method='post',
    request_body=UserRegistrationSerializer,
    responses={200: UserRegistrationSerializer} 
)
@api_view(['POST'])
# @permission_classes([AllowAny])
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
    
    

@swagger_auto_schema(
    method='post',
    request_body=UserLoginSerializer,  # input schema for Swagger
    responses={200: UserLoginSerializer}  # output schema for Swagger
)
@api_view(['POST'])
def login_user(request):
    email = request.data.get('email', '').lower()
    password = request.data.get('password', '')

    # Validate credentials directly in the view
    user = authenticate(email=email, password=password)
    if not user:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    if not user.is_active:
        return Response({"error": "User account is disabled"}, status=status.HTTP_403_FORBIDDEN)
    
    refresh = RefreshToken.for_user(user)
    serializer = UserLoginSerializer(data=request.data, context={'user': user})
    serializer.is_valid(raise_exception=False) 

    return Response({
        "user": serializer.data['user'],
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }, status=status.HTTP_200_OK)


