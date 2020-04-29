from django.contrib.auth.models import User, Group
from django.core.validators import int_list_validator
from rest_framework import serializers
from main.models import Add

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class AddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add
        fields = ['value', 'user']