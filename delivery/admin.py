from django.contrib import admin

# Register your models here.
from .models import  Customer , HubLocation , Distance

admin.site.register([Customer,HubLocation,Distance])
