from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    estimated_time = serializers.ReadOnlyField(source='estimated_time')
    class Meta:
        model = Order
        fields =['id', 'customer', 'items','distance_km','status','estimated_time','created_at']