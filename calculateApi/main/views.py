from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.core.validators import int_list_validator
from django.core.exceptions import ValidationError
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, api_view
from main.serializer import AddSerializer, CalculateSerializer
from main.models import Add, Calculate

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

class CalculateViewSet(viewsets.ModelViewSet):
    serializer_class = CalculateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        instance = Add.objects.get(user=self.request.user)
        all_numbers = instance.value.split(", ")
        
        sum = 0
        for x in all_numbers:
            sum += int(x)

        calculate = Calculate()
        calculate.number = sum
        calculate.user = self.request.user
        calculate.save()

        all_calculations = Calculate.objects.filter(user=self.request.user).order_by('-id')

        print(all_calculations[0])

        return Calculate.objects.filter(user=self.request.user).order_by('-id')

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def calculate(request):
    try:
        instance = Add.objects.get(user=request.user)
    except:
        return HttpResponse("Numbers not provided.")
    
    all_numbers = instance.value.split(", ")
    
    sum = 0
    for x in all_numbers:
        sum += int(x)

    calculate = Calculate()
    calculate.number = sum
    calculate.user = request.user
    calculate.save()

    if request.GET.get('all'):
        all_calculations = Calculate.objects.filter(user=request.user).order_by('-id')

        x = serializers.serialize('json', all_calculations)
        return HttpResponse(x, content_type='application/json')
    else:
        latest_calculation = Calculate.objects.filter(user=request.user).order_by('-id')[0]
        return HttpResponse(latest_calculation)