from django.contrib.admin import register, ModelAdmin
from delivery_app.models import Courier, Delivery, Location

@register(Delivery)
class DeliveryAdmin(ModelAdmin):
    list_display = [
        "delivery_price"
    ]
    search_fields = [
        "code"
    ]

@register(Courier)
class CourierAdmin(ModelAdmin):
    pass

@register(Location)
class LocationAdmin(ModelAdmin):
    pass


