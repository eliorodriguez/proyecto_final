# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Shapes(models.Model):
    
    name = models.CharField(max_length=50)
    family = models.CharField(max_length=50)
    size = models.DecimalField(max_digits=8,decimal_places = 3)
    
    def __str__(self):
    	return str(self.id) + "-" + self.name

class Parts(models.Model):
    
    shape = models.ForeignKey(Shapes, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=512)
    size_x = models.DecimalField(max_digits=8,decimal_places = 3)
    size_y = models.DecimalField(max_digits=8,decimal_places = 3)
    size_z = models.DecimalField(max_digits=8,decimal_places = 3)
    axe_x = models.DecimalField(max_digits=8,decimal_places = 3 , default = 0 )
    axe_y = models.DecimalField(max_digits=8,decimal_places = 3 , default = 0 )
    axe_z = models.DecimalField(max_digits=8,decimal_places = 3 , default = 0 )

    def __str__(self):
        return str(self.id) + "-" + self.shape.name + "-"+self.name

class UnitRelations(models.Model):
    
    part = models.ForeignKey(Parts, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    axe = models.CharField(max_length=1)
    value = models.DecimalField(max_digits=8,decimal_places = 5)

    def __str__(self):
    	return  str(self.part.shape.name) + "-" + self.axe + "-" + self.part.name + "-" + self.name


class BinaryRelations(models.Model):
    
    part_one = models.ForeignKey(Parts, related_name = 'part_one' ,on_delete=models.CASCADE)
    part_two = models.ForeignKey(Parts, related_name = 'part_two' ,on_delete=models.CASCADE)
    axe = models.CharField(max_length=1)
    name = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=8,decimal_places = 5)

    def __str__(self):
        return  str(self.part_one.shape.name) + "-" + self.axe + "-" + self.part_one.name + "-" + self.part_two.name