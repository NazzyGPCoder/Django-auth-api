from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from role.models import UserRole

CustomUser = get_user_model()

class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['role']  # only allow role to be updated

    def validate_role(self, value):
        request_user = self.context['request'].user
        # Only super_admin can assign admin or super_admin
        if value in [UserRole.ADMIN, UserRole.SUPER_ADMIN] and request_user.role != UserRole.SUPER_ADMIN:
            raise serializers.ValidationError("Only super admins can assign admin or super admin roles.")
        return value
    
    
# ----------------------------------------
# Basic user profile serializer
# ----------------------------------------
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email','role', 'username', 'first_name', 'last_name',
            'gender', 'birthdate', 'profile_image', "bio", "phone", 
            "address_line", "city", "state", "country",
            'created_at'
        ]
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email','password', 'username', 'first_name', 'last_name',
            'gender', 'birthdate', 'profile_image', "bio", "phone", 
            "address_line", "city", "state", "country",
            'created_at'
        ]
        extra_kwargs = {
            'username': {'required': False},
            'birthdate': {'required': False},
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

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'email','role','first_name', 'last_name', 'gender', 'birthdate',
            'profile_image', 'bio', 'phone', 'address_line',
            'city', 'state', 'country'
        ]