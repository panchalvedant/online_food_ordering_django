from django.contrib import admin

# Register your models here.
from .models import user,customer,alert,Item_feedback
admin.site.register(user)
admin.site.register(customer)
admin.site.register(alert)
admin.site.register(Item_feedback)