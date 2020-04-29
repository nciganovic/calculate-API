from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from main.serializer import UserSerializer, GroupSerializer, AddSerializer
from main.models import Add

class AddViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    #queryset = Add.objects.all()
    serializer_class = AddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the adds
        for the currently authenticated user.
        """
        this_user = self.request.user
        return Add.objects.filter(user=this_user)

    def create(self, validated_data):
        value = request.POST['value']
        print("VALUE => ", value)
        return HttpResponse("Here's the text of the Web page.")

AddViewSet.as_view({'get': 'list', 'post':'create'}) # For: /api/subscriber
AddViewSet.as_view({'get': 'retrieve', 'put':'update'}) # For: /api/subscriber/1