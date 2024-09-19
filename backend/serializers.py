from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = CustomUser
    fields = ['email', 'name', 'password', 'is_active', 'is_staff']
    extra_kwargs = {
      'password': {'write_only': True}
    }

  def create(self, validated_data):
    user = CustomUser(
      email=validated_data['email'],
      name=validated_data.get('name', ''),
      is_active=validated_data.get('is_active', True),
      is_staff=validated_data.get('is_staff', False)
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

class CreateUserSerializer(CustomUserSerializer):
  def create(self, validated_data):
    return super().create(validated_data)

class CreateStaffUserSerializer(CustomUserSerializer):
  def create(self, validated_data):
    validated_data['is_staff'] = True
    return super().create(validated_data)

class CreateSuperUserSerializer(CustomUserSerializer):
  def create(self, validated_data):
    validated_data['is_staff'] = True
    validated_data['is_superuser'] = True
    return super().create(validated_data)
