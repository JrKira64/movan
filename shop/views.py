# Create your views here.
from rest_framework.response import Response
from rest_framework import views,viewsets
from .models import *
from .serializers import *
from core.crudview import  CRUDView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User


class RoadtripView(CRUDView):
    queryset = Roadtrip.objects.all().order_by("-id")
    serializer_class=RoadtripSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['From','to','Date']
    
    def get(self,request,id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request, *args, **kwargs):
        RoadtripSerializers.Meta.depth = 0
        data = request.data
        wrappers = super().create(request, *args, **kwargs)
        return wrappers

class RegisterView(views.APIView):
    def post(self,request):
        serializers =UserSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"error":False,"message":f"user is created for '{serializers.data['username']}' ","data":serializers.data})
        return Response({"error":True,"message":"A user with that username already exists! Try Anather Username"})


class MyCart(viewsets.ViewSet):
    def list(self, request):
        query = Cart.objects.filter(customer=request.user.profile)
        serializers = CartSerializer(query,many=True)
        all_data=[]
        for cart in serializers.data:
            cart_booking = CartBooking.objects.filter(cart=cart["id"])
            cart_booking_serializer = CartBookingSerializer(cart_booking,many=True)
            cart["cartbooking"] = cart_booking_serializer.data
            all_data.append(cart) 
        return Response(all_data)


class OldOrders(viewsets.ViewSet):
  
    def list(self,request):
        query = Order.objects.filter(cart__customer = request.user.profile)
        serializers = OrderSerializer(query,many=True)
        all_data = []
        for order in serializers.data:
            cartbooking = CartBooking.objects.filter(cart_id=order['cart']['id'])
            cartbooking_serializer = CartBookingSerializer(cartbooking,many=True)
            order['cartbooking'] = cartbooking_serializer.data
            all_data.append(order)
        return Response(all_data)
    def retrieve(self,request,pk=None):
        try:
            queryset = Order.objects.get(id=pk)
            serializers = OrderSerializer(queryset)
            data = serializers.data
            all_date=[]
            cartbooking = CartBooking.objects.filter(cart_id=data['cart']['id'])
            cartbooking_serializer = CartBookingSerializer(cartbooking,many=True)
            data['cartbooking'] = cartbooking_serializer.data
            all_date.append(data)
            response_message = {"error":False,"data":all_date}
        except:
            response_message = {"error":True,"data":"No data Found for This id"}

        return Response(response_message)


    def destroy(self,request,pk=None):
        try:
            order_obj=Order.objects.get(id=pk)
            cart_obj = Cart.objects.get(id=order_obj.cart.id)
            order_obj.delete()
            cart_obj.delete()
            responsemessage = {"erroe":False,"message":"Order delated","order id":pk}
        except:
            responsemessage = {"erroe":True,"message":"Order Not Found"}
        return Response(responsemessage)

    

    def create(self,request):
        cart_id = request.data["cartId"]
        cart_obj = Cart.objects.get(id=cart_id)
        address = request.data["address"]
        mobile = request.data["mobile"]
        email = request.data["email"]
        cart_obj.complit=True
        cart_obj.save()
        created_order = Order.objects.create(
            cart=cart_obj,
            address=address,
            mobile=mobile,
            email=email,
        )
        return Response({"message":"order Resebed","cart id":cart_id,"order id":created_order.id})


class Addtocart(views.APIView):
    
    def post(self,request):
        roadtrip_id = request.data['id']
        roadtrip_obj = Roadtrip.objects.get(id=roadtrip_id)
        #print(roadtrip_obj,"roatrip_obj")        
        cart_cart = Cart.objects.filter(customer=request.user.profile).filter(complit=False).first()
        booking_obj = CartBooking.objects.filter(roadtrip__id=roadtrip_id).first()
        
        try:
            if  cart_cart:
                # print(cart_cart)
                # print("OLD CART")
                this_product_in_cart = cart_cart.cartbooking_set.filter(roadtrip=roadtrip_obj)
                if this_booking_in_cart.exists():
                    # print("OLD CART PRODUCT--OLD CART")
                    cartbook_ing = CartBooking.objects.filter(roadtrip=roadtrip_obj).filter(cart__complit=False).first()
                    cartbook_ing.save() 
                    cart_cart.save() 
                else:
                    # print("NEW CART PRODUCT CREATED--OLD CART")
                    cart_booking_new=CartBooking.objects.create(
                        cart = cart_cart, 
                    )
                    cart_booking_new.Roadtrip.add(roadtrip_obj)
                    cart_cart.save()
            else:
                # print(cart_cart)
                # print("NEW CART CREATED")
                Cart.objects.create(customer=request.user.profile,complit=False)
                new_cart = Cart.objects.filter(customer=request.user.profile).filter(complit=False).first()
                cart_booking_new=CartBooking.objects.create(
                        cart = new_cart,
                    )
                cart_booking_new.Roadtrip.add(roadtrip_obj)
                # print("NEW CART PRODUCT CREATED")    
                
                new_cart.save()

            response_mesage = {'error':False,'message':"Roadtrip add to card successfully","roadtripid":roadtrip_id}
        
        except:
            response_mesage = {'error':True,'message':"Roadtrip Not add!Somthing is Wromg"}

        return Response(response_mesage)