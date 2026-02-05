import math
from django.db import models
from django.conf import settings
from dish.models import Dish


class Order(models.Model):
    STATUS_CHOICES = [
        ('cart', 'Savatda'),
        ('pending', 'Kutilmoqda (Tasdiqlangan)'),
        ('ready', 'Tayyor'),
        ('delivered', 'Yetkazildi')
    ]
    default = 'cart'  # Mahsulot qo'shilganda avval savatga tushadi

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    distance_km = models.FloatField(default=0.0, help_text="Masofa (km)")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cart')

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username} ({self.status})"

    @property
    def get_total_price(self):
        """Buyurtmadagi barcha elementlarning narxini qo'shib chiqadi"""
        return sum(item.get_item_total for item in self.items.all())

    @property
    def estimated_delivery_time(self):
        # 1. Savatdagi taomlar sonini olamiz
        total_items = sum(item.quantity for item in self.items.all())


        import math
        prep_time = math.ceil(total_items / 4) * 5
        travel_time = self.distance_km * 3
        total_time = prep_time + travel_time
        return total_time


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def get_item_total(self):
        return self.dish.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.dish.name}"