from rest_framework import serializers as serializers 
from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.password_validation import validate_password


CustomUser = get_user_model()

# ----------------------------------------
# Basic user profile serializer
# ----------------------------------------

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'gender', 'birthdate', 'profile_image', "bio", "phone", 
            "address_line", "city", "state", "country",
            'created_at'
        ]
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'username','password', 'first_name', 'last_name',
            'gender', 'birthdate', 'profile_image', "bio", "phone", 
            "address_line", "city", "state", "country",
            'created_at'
        ]
        extra_kwargs = {
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'gender': {'required': False},
            'birthdate': {'required': False},
            'bio': {'required': False},
            'phone': {'required': False},
            'address_line': {'required': False},
            'city': {'required': False},
            'state': {'required': False},
            'country': {'required': False},
            'profile_image': {'required': False, 'allow_null': True},
        }

    def validate_email(self, value):
        value = value.lower()
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        username = validated_data.get('username') or validated_data['email'].split('@')[0]
        user = CustomUser.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            gender=validated_data.get('gender'),
            birthdate=validated_data.get('birthdate'),
            profile_image=validated_data.get('profile_image'),
        )
        return user