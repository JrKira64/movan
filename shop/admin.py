from django.contrib import admin

# Register your models here.
from .models import *


class RoadtripAdmin(admin.ModelAdmin):
    list_display = ("id","From","to")
admin.site.register(Roadtrip,RoadtripAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=("id","customer","complit","date")
admin.site.register(Cart,CartAdmin)

admin.site.register(CartBooking)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id","prouser")
admin.site.register(Profile,ProfileAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","cart","date","address","email", "mobile")
admin.site.register(Order,OrderAdmin)