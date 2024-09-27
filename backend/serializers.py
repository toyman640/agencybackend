from rest_framework import serializers
from .models import CustomUser, Agency

class CustomUserSerializer(serializers.ModelSerializer):

  class Meta:
    model = CustomUser
    fields = ['id', 'email', 'name', 'password', 'is_active', 'is_staff']
    extra_kwargs = {
      'password': {'write_only': True}
    }

  def create(self, validated_data):
    if not validated_data.get('is_staff', False):
      validated_data['is_active'] = False
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


class AgencySerializer(serializers.ModelSerializer):
  created_by = serializers.SerializerMethodField()

  class Meta:
    model = Agency
    fields = ['id','agency_name', 'address', 'phone_number', 'email', 'created_by']

  def get_created_by(self, obj):
    return {
      "id": obj.created_by.id,
      "name": obj.created_by.name,
      "email": obj.created_by.email,
      "is_active": obj.created_by.is_active,
    }
