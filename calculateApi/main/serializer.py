from django.contrib.auth.models import User, Group
from django.core.validators import int_list_validator
from rest_framework import serializers
from main.models import Add, Calculate

class AddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add
        fields = ['value']
        