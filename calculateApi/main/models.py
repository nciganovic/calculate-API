from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator

class Add(models.Model):
    value = models.CharField(max_length=255, validators=[int_list_validator(sep=', ', message=None, code='invalid', allow_negative=True)]) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name_plural = "Adds"

class Calculate(models.Model):
    number = models.IntegerField() 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.number)
    
    class Meta:
        verbose_name_plural = "Calculations"

class History(models.Model):
    array = models.CharField(max_length=255, validators=[int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    calculations = models.CharField(max_length=255, validators=[int_list_validator(sep=', ', message=None, code='invalid', allow_negative=False)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.user}'
    
    class Meta:
        verbose_name_plural = "History"