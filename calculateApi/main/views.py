import json
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.core.validators import int_list_validator
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, api_view
from main.serializer import AddSerializer
from main.models import Add, Calculate, History

def make_int_array_list(element, array_list):
    """
    Converts [{'array': '1, 99, 13, 45', 'calculations': '78, 12'}]
    To [{'array': [1, 99, 13, 45], 'calculations': [78, 12]}]
    """
    for x in array_list:
        x[element] = x[element].split(", ")
        int_arr = []
        for y in x[element]:
            int_arr.append(int(y))
        x[element] = int_arr

class AddViewSet(viewsets.ModelViewSet):
    serializer_class = AddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        this_user = self.request.user
        return Add.objects.filter(user=this_user)

    def create(self, validated_data):
        this_value = validated_data.POST['value']
        validator = int_list_validator(sep=', ', message=None, code='invalid', allow_negative=True)

        try:
            validator(this_value)
            try: 
                instance = Add.objects.get(user=self.request.user)
                instance.value = instance.value + ", " + this_value
                instance.save()
                return HttpResponse(status=201)
            except:
                add = Add()
                add.value = this_value
                add.user = self.request.user
                add.save()
                return HttpResponse(status=201)
            
        except:
            return HttpResponse("Invalid data", status=406)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def calculate(request):
    try:
        instance = Add.objects.get(user=request.user)
    except:
        return HttpResponse("Numbers not provided.", status=406)
    
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
        calculation_array = []
        for cal in all_calculations:
            num_dict = {}
            num_dict["number"] = cal.number
            calculation_array.append(num_dict)
        
        calculation_array = json.dumps(calculation_array)
        return HttpResponse(calculation_array, content_type='application/json', status=200)
    else:
        latest_calculation = Calculate.objects.filter(user=request.user).order_by('-id')[0]
        return HttpResponse(latest_calculation, status=200)

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def reset(request):
    try:
        all_calculations = Calculate.objects.filter(user=request.user)
        adds = Add.objects.get(user=request.user)

        comma_sep_calculations = ""
        for cal in all_calculations :
            comma_sep_calculations += str(cal.number) + ", "
        comma_sep_calculations = comma_sep_calculations[:-2]

        history = History()
        history.array = adds
        history.calculations = comma_sep_calculations
        history.user = request.user
        history.save()

        all_calculations.delete()
        adds.delete()

        return HttpResponse(status=201)
    except:
        return HttpResponse("You dont have any calculations yet.", status=406)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def history(request):
    if request.GET.get('id'):
        this_id = request.GET.get('id')
        single_history = History.objects.filter(user=request.user, id=this_id)
        if single_history:
            single_history_list = list(single_history.values("id", "array", "calculations"))
            make_int_array_list("array", single_history_list)
            make_int_array_list("calculations", single_history_list)
            return JsonResponse(single_history_list, safe=False, status=200)
        else:
            return HttpResponse("This element does not exist", status=404)
    else:
        all_history = History.objects.filter(user=request.user).order_by("-id")
        if all_history:
            history_list = list(all_history.values("id", "array", "calculations"))

            make_int_array_list("array", history_list)
            make_int_array_list("calculations", history_list)
                
            return JsonResponse(history_list, safe=False, status=200)
        else:
            return HttpResponse("History is empty", status=404)
