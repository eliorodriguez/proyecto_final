# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from exploration.models import *

import json
import numpy as np

from django.conf import settings
from exploration import tools


def index(request):
	model = json.load(open(settings.MEDIA_ROOT+'models/chairs.json'))
	#shape = Shapes.objects.order_by('size').first()
	shape = Shapes.objects.get(name = 11)
	parts = Parts.objects.filter( shape = shape.id ).values('path','name','label')

	scales = {} 

	if request.method == 'POST':

		x = float(request.POST.get("x"))
	
		label = int(request.POST.get("label"))
		scales = {label:x}
		labels = [1,2,3]
		part1 = Parts.objects.filter(shape = shape.id , label = label ).first()
		new_size_part = float(part1.size_x) + float(x) 
		for i in labels :
			if label != i :
				part2 = Parts.objects.filter(shape = shape.id , label = str(i) ).first()
				if label < i :
					bi_current = new_size_part / float(part2.size_x) 
					bi_opt = tools.getHighProbability( model["pdf"],label,i,bi_current)
					relation = BinaryRelations.objects.filter( part_one = part1.id,
								                           part_two = part2.id ,
								                           name = "scale" , 
								                           axe = "1" )

					if relation.count() and abs(float(relation.first().value) - bi_opt) > 0.01:
						bi_opt = float(relation.first().value)

					scales[i] = (( new_size_part / bi_opt ) - float(part2.size_x) ) 

				else :
					bi_current = float(part2.size_x) / new_size_part 
					bi_opt = tools.getHighProbability( model["pdf"],label,i,bi_current)
					relation = BinaryRelations.objects.filter( part_one = part2.id,
									                           part_two = part1.id ,
									                           name = "scale" , 
									                           axe = "1" )

					if relation.count() and abs(float(relation.first().value) - bi_opt) > 0.01:
						bi_opt = float(relation.first().value)-0.09

					scales[i] = (( new_size_part * bi_opt ) - float(part2.size_x) ) 


				
				print new_size_part

	return render(request, 'editing/index.html', { 'parts' : json.dumps( list(parts)) , 'scales' : json.dumps(scales) } )