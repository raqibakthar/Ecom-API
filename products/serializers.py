from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer
from .models import Product,Order,OrderItems,ShippingAddress,Review

class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
    def get_reviews(self,obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews,many=True) 
        return serializer.data

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItems
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):

    order = serializers.SerializerMethodField(read_only = True)
    ShippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Order
        fields = '__all__'
    
    def get_order(self,obj):
        items = obj.orderitems_set.all()
        serializer = OrderItemSerializer(items,many=True)
        return serializer.data
    def get_ShippingAddress(self,obj):
        try:
            address = ShippingAddressSerializer(obj.shippingAddress,many=False).data
        except:
            address = False
        return address
    def get_user(self,obj):
        user = obj.user
        serializer = UserSerializer(user,many=False)
        return serializer.data

class ShippingAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingAddress
        fields = '__all__'