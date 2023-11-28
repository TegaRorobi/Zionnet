from django.contrib import admin
from .models import *

class MarketplaceAdmin(admin.ModelAdmin):
    model = MarketPlace
    list_display = 'name', 'cover_image'
