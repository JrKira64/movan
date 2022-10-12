from django.urls import path,include
from .views import *
from rest_framework import routers

route =routers.DefaultRouter()
route.register('orders',OldOrders, basename="orders")
route.register("booking",MyCart,basename="booking")

urlpatterns = [
    path("", include(route.urls)),
    path("roadtrip/",RoadtripView.as_view(),name="roadtrip"),
    path("roadtrip/<int:id>/",RoadtripView.as_view(),name="roadtripdetal"),
    path("addtobooking/",Addtocart.as_view(),name="booking"),
    path("register/",RegisterView.as_view(),name="register"),
]