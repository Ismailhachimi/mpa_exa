

from rest_framework.serializers import ModelSerializer
from accounts import models

from django.contrib.auth.models import Group


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)


class RetrieveUserSerializer(ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = models.User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active',
                  'joined_at', 'last_login', 'groups']


class ListUserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'joined_at']


class CreateUserSerializer(ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = models.User
        fields = ['email', 'first_name', 'last_name', 'password', 'groups']
        extra_kwargs = {
            'groups': {'required': True},
        }


class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'read_only': True}
        }
