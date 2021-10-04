from django.contrib import admin

# Register your models here.

from .models import Item,Category,OrderProduct,restaurant,cart,favourite
admin.site.register(Category)
admin.site.register(OrderProduct)
admin.site.register(Item)
admin.site.register(restaurant)
admin.site.register(cart)
admin.site.register(favourite)