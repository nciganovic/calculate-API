from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator

class Add(models.Model):
    value = models.CharField(max_length=255, validators=[int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)]) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.value

class Calculate(models.Model):
    number = models.IntegerField() 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.number)
