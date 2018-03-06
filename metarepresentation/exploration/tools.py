import numpy as np
from sklearn.neighbors import BallTree
from scipy.stats.kde import gaussian_kde 
from django.conf import settings
import re
from .models import *
from decimal import Decimal
import random
from scipy.signal import find_peaks_cwt

from sklearn.cluster import MeanShift, estimate_bandwidth

def swap(label1,label2):
    return label2,label1
# def evaluate_updf(model,label,axe):
#     file = open(settings.MEDIA_ROOT + "distributions/"+model+"/updf_"+str(axe)+".txt", "r")
#     data = []
#     for line in file:
#         line = line.replace("[","")
#         line = line.replace("]","")
#         values = line.split(",")
#         data.append([ float(v) for v in values ])
#     return data[2*label-2],data[2*label-1]

# def evaluate_pdf(model,label1,label2,axe):
#     file = open(settings.MEDIA_ROOT + "distributions/"+model+"/pdf.txt", "r")
#     data = []
#     for line in file:
#         if len(line) > 5 :
#             line = line.replace("[","")
#             line = line.replace("]","")
#             #print line
#             values = line.split(",")
#             data.append([ float(v) for v in values ])
#         else :
#             data.append([])
#     index = (label1-1)*6+label2*2
#     return data[index-2],data[index-1]

def plot(x,y,x1,y1):
    data = []
    for i in range(len(x)):
        if i > 0 and x[i-1] < x1 and x1 < x[i] and x1 != 0 :
            data.append({"x": x1  , "y" :  y1 , "color" : "green", "markerSize" : 10 }) #"indexLabel" : "Aqui" })

        data.append({"x":x[i] , "y" : y[i] })
    return data

def evaluate(points,x1,x2):

    p5 = np.percentile(points,5) 
    p95 = np.percentile(points,95) 
    #kde = gaussian_kde(points,0.15)#0.16
    #print (p95-p5)*0.15
    #kde = gaussian_kde(points,0.15*(p95-p5))
    kde = gaussian_kde(points,0.15*(p95-p5))
    #kde = gaussian_kde(points,0.038*(p95-p5))#0.03 0.08 0.005
    y1 = kde.evaluate(x1)
    y2 = kde.evaluate(x2)
    return y1,y2

def getPoints(pdf):
    #print pdf
    ind = pdf["N"]
    pts = np.zeros((pdf["N"]));
    perm = np.array(pdf["perm"])
    centers = np.array(pdf["centers"])
    pts[ perm[[np.array(range(0,ind))+ind]]] = centers[ np.array(range(0,ind)) + ind ];
    return pts[:ind]

def ushow(updf,label,relation, value ):
    points = getPoints(updf[(label-1)+(relation-1)*5])
    #print points
    min_point = points.min();
    max_point = points.max();
    range_points = [min_point, max_point];
    if min_point == max_point :
        range_points[0] = min_point - .05;
        range_points[1] = min_point + .05;
    else :
        range_points[0] = range_points[0] - .05*(range_points[1]-range_points[0]);
        range_points[1] = range_points[1] + .05*(range_points[1]-range_points[0]);
    N = 200 ;
    x1 = np.round(np.linspace(range_points[0], range_points[1], N),4);
    x2 = points
    #x2 = points.tolist()

    #y1 , y2 = evaluate_updf("chairs",label,relation)
    #y1 , y2 = evaluate(points,x1,x2)
    #y2 = evaluate(points,x2)
    p5 = np.percentile(points,5) 
    p95 = np.percentile(points,95) 
    #kde = gaussian_kde(points,0.15)#0.16
    #print (p95-p5)*0.15
    #kde = gaussian_kde(points,0.15*(p95-p5))
    kde = gaussian_kde(points,0.18*(p95-p5))
    #kde = gaussian_kde(points,0.038*(p95-p5))#0.03 0.08 0.005
    y1 = kde.evaluate(x1)
    y2 = kde.evaluate(x2)



    #x1 = x1.tolist()
    # data1 = []
    # if value != 0 :
    #     data1.append({"x": value  , "y" :  kde.evaluate(value)[0] , "color" : "green", "markerSize" : 10 }) #"indexLabel" : "Aqui" })
    
    # for i in range(len(x1)):
    #     data1.append({"x":x1[i] , "y" : y1[i] })
    data1 = plot(x1,y1,value,kde.evaluate(value)[0])
    data2 = plot(x2,y2,value,kde.evaluate(value)[0])


    # data2 = []
    # for i in range(len(x2)):
    # 	data2.append({"x":x2[i] , "y" : y2[i]})

    return data1,data2


def show(pdf,label1,label2,axe,value , relation):
    if label1 > label2 :
        label1 , label2 = swap(label1,label2)
    print relation
    if relation == "scale" :
        points = getPoints(pdf[(label1-1)+(label2-1)*5])
    elif relation == "angle" :
        points = getPoints(pdf[240])
    print len(points)
    min_point = points.min();
    max_point = points.max();
    range_points = [min_point, max_point];
    if min_point == max_point :
        range_points[0] = min_point - .05;
        range_points[1] = min_point + .05;
    else :
        range_points[0] = range_points[0] - .05*(range_points[1]-range_points[0]);
        range_points[1] = range_points[1] + .05*(range_points[1]-range_points[0]);
    N = 200 ;
    x1 = np.round(np.linspace(range_points[0], range_points[1], N),4);
    x2 = points
    #x2 = points.tolist()
    #y1 , y2 = evaluate_pdf("chairs",label1,label2,1)
    
    p5 = np.percentile(points,5) 
    p95 = np.percentile(points,95) 
    #kde = gaussian_kde(points,0.15)#0.16
    #print (p95-p5)*0.15
    #kde = gaussian_kde(points,0.03*(p95-p5))
    kde = gaussian_kde(points,0.03*(p95-p5))
    #kde = gaussian_kde(points,0.038*(p95-p5))#0.03 0.08 0.005
    y1 = kde.evaluate(x1)
    y2 = kde.evaluate(x2)

    data1 = plot(x1,y1,value,kde.evaluate(value)[0])
    data2 = plot(x2,y2,value,kde.evaluate(value)[0])
    # x1 = x1.tolist()
    # data1 = []
    # if value != 0 :
    #     data1.append({"x": value  , "y" :  kde.evaluate(value)[0] , "color" : "green" , "indexLabel" : "Aqui" })
    # for i in range(len(x1)):
    # 	data1.append({"x":x1[i] , "y" : y1[i]  })

    # data2 = []
    # for i in range(len(x2)):
    # 	data2.append({"x":x2[i] , "y" : y2[i]})

    return data1,data2

def setTitle(label1 , label2 , relation ):
    chart_title = "" 
    if label1 and label2 :
        chart_title += relation + " Relation ( Label "+str(label1)+" - Label "+str(label2) + " )"        
    elif label1 :
        chart_title += "Extent Relation ( Label "+str(label1) + ")"

    return chart_title 


def getHighProbability( pdf,label1,label2,x):
    
    if label1 > label2 :
        label1 , label2 = swap(label1,label2)
    points = getPoints(pdf[(label1-1)+(label2-1)*5])
    min_point = points.min();
    max_point = points.max();
    range_points = [min_point, max_point];
    if min_point == max_point :
        range_points[0] = min_point - .05;
        range_points[1] = min_point + .05;
    else :
        range_points[0] = range_points[0] - .05*(range_points[1]-range_points[0]);
        range_points[1] = range_points[1] + .05*(range_points[1]-range_points[0]);
    p5 = np.percentile(points,5) 
    p95 = np.percentile(points,95)

    bandwidth = 0.03*(p95-p5)
    kde = gaussian_kde(points,bandwidth)
    N = 200 ;
    x1 = np.round(np.linspace(range_points[0], range_points[1], N),4);
    y1 = kde.evaluate(x1)
    
    peaks =  x1[find_peaks_cwt(y1,np.arange(1,20))]
    value = x1[(np.abs(peaks-float(x))).argmin()]


    return value

def createUnitRelations():
    shapes = Shapes.objects.all()
    for shape in shapes :
        parts = Parts.objects.filter(shape = shape.id)
        is_leg = 0
        for part in parts :
            if is_leg < 1 or part.label != "1" :
                if part.label == "1" :
                    is_leg += 1

                UnitRelations.objects.get_or_create(part = part, name = "extent" , axe = "1" , value = round(part.size_x / shape.size,3) )
                UnitRelations.objects.get_or_create(part = part , name = "extent" , axe = "2" , value = round(part.size_y / shape.size,3) )
                UnitRelations.objects.get_or_create(part = part , name = "extent" , axe = "3" , value = round(part.size_z / shape.size,3) )
         

def createBinaryRelations():
    shapes = Shapes.objects.all()
    for shape in shapes :
        parts = Parts.objects.filter(shape = shape.id)
        is_leg = 0
        for p in parts :
            for q in parts :
                if p.id != q.id  and p.label < q.label : 
                    if (p.label == "1" and is_leg < 2 ) or p.label != "1" : 
                        is_leg += 1
                        BinaryRelations.objects.get_or_create(part_one = p,
                                                        part_two = q ,
                                                        name = "scale" , 
                                                        axe = "1" , 
                                                        value = round(p.size_x / q.size_x,3) )
                        
                        # BinaryRelations.objects.get_or_create(part_one = p,
                        #                                 part_two = q ,
                        #                                 name = "angle" , 
                        #                                 axe = "1" , 
                        #                                 value = round(random.uniform(0, 1),3) )


