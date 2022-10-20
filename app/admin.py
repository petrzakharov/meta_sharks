from django.contrib import admin
from .models import Color, ModelType, Brand, Order

admin.site.register(Color)
admin.site.register(ModelType)
admin.site.register(Brand)


@admin.register(Order)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('color', 'model', 'quantity', 'date',)
