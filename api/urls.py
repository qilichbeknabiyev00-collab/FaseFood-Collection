from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dish.views import DishViewSet
from order.views import OrderViewSet

router = DefaultRouter()
router.register(r'dishes', DishViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('accaunt/login', include(router.urls)),
]