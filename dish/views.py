from users.permissions import IsWaiterUser, IsAdminUser
from rest_framework import views, permissions
from rest_framework import viewsets, generics
from .serializers import DishSerializer
from django.shortcuts import render
from order.models import Order
from .models import Dish

def get_permissions(self):
     if self.action in ['list', 'retrieve']:
        return [permissions.AllowAny()]
     elif self.action in ['create', 'update', 'partial_update', 'destroy']:
        return [IsWaiterUser() | IsAdminUser()]
     return [permissions.IsAuthenticated()]

def dish_list(request):
    dishes = Dish.objects.filter(is_available=True)
    cart = None
    if request.user.is_authenticated:
        cart = Order.objects.filter(customer=request.user, status='cart').first()
    return render(request, 'menu/dish_list.html', {
        'dishes': dishes,
        'cart': cart,
    })

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer