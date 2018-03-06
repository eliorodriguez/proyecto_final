# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

class ShapesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Shapes, ShapesAdmin)


admin.site.register(Parts)
admin.site.register(UnitRelations)
admin.site.register(BinaryRelations)