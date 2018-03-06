# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


from django.conf import settings


def index(request):
	return render(request, 'index.html',{})