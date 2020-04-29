from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator

class Add(models.Model):
    value = models.CharField(max_length=255, validators=[int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)]) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.value

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
