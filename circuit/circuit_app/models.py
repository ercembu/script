from django.db import models
# Create your models here.

class Circuit_hold(models.Model):
	name = models.CharField(max_length=100)
	circuit = models.BinaryField(max_length=1000)
	components = models.BinaryField(max_length=1000,null=True)
	lastID = models.IntegerField(default=0)
	input_set = models.BooleanField(default=False)
	flag = models.BooleanField(default= False)
