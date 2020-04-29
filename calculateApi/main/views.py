from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.core.validators import int_list_validator
from django.core.exceptions import ValidationError
from rest_framework import viewsets, permissions, generics
from main.serializer import AddSerializer
from main.models import Add

class AddViewSet(viewsets.ModelViewSet):
    serializer_class = AddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        this_user = self.request.user
        return Add.objects.filter(user=this_user)

    def create(self, validated_data):
        this_value = validated_data.POST['value']
        validator = int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)

        try:
            validator(this_value)

            try: 
                instance = Add.objects.get(user=self.request.user)
                instance.value = instance.value + ", " + this_value
                instance.save()
            except:
                add = Add()
                add.value = this_value
                add.user = self.request.user
                add.save()
                return HttpResponse("")
            
            return HttpResponse("")
        except ValidationError as e:
            print(e)
            return HttpResponse("Invalid Data")
