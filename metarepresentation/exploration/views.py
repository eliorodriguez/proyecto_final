# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from exploration.models import *

import json
import numpy as np
import tools

from django.conf import settings



def index(request):
	#tools.createUnitRelations()
	#tools.createBinaryRelations()
	#q =  UnitRelations.objects.filter(axe = "1" , part__label = 1 ).order_by('value')

	#q =  BinaryRelations.objects.filter(axe = "1" , part_one__label = 2 , part_two__label = 3 ).order_by('value')
	# for i in q :
	# 	print i.value

	model = json.load(open(settings.MEDIA_ROOT+'models/chairs.json'))
	label1 = 1
	label2 = ""
	#default_shape = 9
	shape = Shapes.objects.order_by('size').first()
	data1 , data2 = tools.ushow(model["updf"],label1,1 , 0 )
	chart_title = "Extent Relation | Label "+str(label1)
	relation = "scale"
	value = -1

	if request.method == 'POST':

		label1 = request.POST.get("label1")
		label2 = request.POST.get("label2")
		relation = request.POST.get("relation")

		if "reload" in request.POST :
			if(label1 and label2) :
				data1 , data2 = tools.show(model["pdf"],int(label1),int(label2),0,0,relation)
				
			elif(label1) :
				data1 , data2 = tools.ushow(model["updf"],int(label1),1,0)
		else :
			value = float(request.POST.get("x"))
			if label1 and label2 :
				#busqueda binaria
				if int(label1) > int(label2) :
					label1,label2 = tools.swap(label1,label2)
				if "next" in request.POST :
					query = BinaryRelations.objects.filter( axe = "1" , name = relation ,
														part_one__label = label1 , 
														part_two__label = label2,
														value__gt = value ).order_by('value')
				elif "back" in request.POST :
					query = BinaryRelations.objects.filter(axe = "1" , name = relation ,
														 value__lt = value , 
														 part_one__label = label1 ,
														 part_two__label = label2 ).order_by('-value')
				
				if query.count() :
					value = query.first().value
					shape = query.first().part_one.shape
				else :
					value = -1

				data1 , data2 = tools.show(model["pdf"],int(label1),int(label2),1,float(value),relation)

			elif label1 :
				#busqueda simple
				if "next" in request.POST :

					query = UnitRelations.objects.filter(axe = "1" , 
													 value__gt = value , 
													 part__label = label1 ).order_by('value')

				elif "back" in request.POST :

					query = UnitRelations.objects.filter(axe = "1" , 
													 value__lt = value , 
													 part__label = label1 ).order_by('-value')
		
				if query.count() :
					value = query.first().value
					shape = query.first().part.shape
				
				else :
					value = -1 
				data1 , data2 = tools.ushow(model["updf"],int(label1),1,float(value))
			
		chart_title = tools.setTitle(label1,label2,relation)


	parts = Parts.objects.filter( shape = shape.id ).values('path','name','label')
	return render(request, 'exploration/index.html', { 	'data1': json.dumps(data1) ,
											'data2': json.dumps(data2) ,
											'chart_title' : chart_title ,
											'parts' :json.dumps( list(parts)) ,
											'label1' : label1,
											'label2' : label2,
											'value' : value ,
											'shape' : shape , 
											'model' : json.dumps(model["pdf"]) ,
											'relation' : relation } )



def save(request) :
	
	if request.method == 'POST':
		
		if "save" in request.POST :
				name = request.POST["shape_name"]
				size = request.POST["shape_size"]
				new_shape = Shapes(name= name ,family="Chairs",size = size )

				new_shape.save()
			
		elif "save_parts" in request.POST :
			shape_name = request.POST["shape_name"]
			x = request.POST.getlist("x[]")
			y = request.POST.getlist("y[]")
			z = request.POST.getlist("z[]")
			labels = request.POST.getlist("labels[]")
			id_shape = Shapes.objects.filter(name=shape_name).first()	
			if id_shape :
				for i in range(0,6):
					if labels[i] == "3" :
						path = "chairs/"+shape_name+"/1.obj"
						name = "back"
					elif labels[i] == "2" :
						path = "chairs/"+shape_name+"/2.obj"
						name = "seat"
					else :
						path = "chairs/"+shape_name+"/3.obj"
						name = "leg" 
					new_part = Parts(shape = id_shape , label = labels[i] , name = name ,  path = path , size_x = float(x[i]) , size_y = float(y[i]) , size_z = float(z[i]) )	
					new_part.save()
