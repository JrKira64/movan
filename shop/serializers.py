from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",'username','password','first_name','last_name','email')
        extra_kwargs = {'password':{'write_only':True,'required':True}}
    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        Profile.objects.create(prouser=user) 
        return user


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['prouser']

    def validate(self,attrs):
        attrs['prouser'] = self.context['request'].user
        return attrs

    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['prouser'] = UserSerializer(instance.prouser).data
        return response

class RoadtripSerializers(serializers.ModelSerializer):
    class Meta:
        model = Roadtrip
        fields = "__all__"
        depth = 1

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 1

class CartBookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartBooking
        fields = "__all__"
        depth = 1

class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        depth = 1