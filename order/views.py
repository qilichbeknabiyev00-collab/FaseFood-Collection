from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDate
from django.core.paginator import Paginator
from .models import Order,Dish,OrderItem
from .serializers import OrderSerializer
from rest_framework import viewsets
from django.shortcuts import render
from django.db.models import Q

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

def add_to_order(request, dish_id, action):
    dish = get_object_or_404(Dish, id=dish_id)

    order, created = Order.objects.get_or_create(
        customer=request.user,
        status='cart',
        defaults={'distance_km': 0.0}
    )
    order_item, item_created = OrderItem.objects.get_or_create(order=order, dish=dish)
# fiff
    if action == 'add':
        if not item_created:
            order_item.quantity += 1
            order_item.save()
        else:
            order_item.quantity = 1
            order_item.save()

    elif action == 'remove':
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
        else:
            order_item.delete()

    return redirect(request.META.get('HTTP_REFERER', 'menu_page_nomi'))

def view_cart(request):
    order = Order.objects.filter(customer=request.user, status='cart').first()
    return render(request, 'cart.html', {'order': order})

def checkout(request):
    if request.method == "POST":
        order = Order.objects.filter(customer=request.user, status='cart').first()
        if order:
            order.status = 'pending'
            order.save()
            return redirect('my_orders')
    return redirect('view_cart')

def my_orders(request):
    orders = Order.objects.filter(customer=request.user).exclude(status='cart').order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

def profile_view(request):
    orders_count = Order.objects.filter(customer=request.user).count()

    return render(request, 'profile.html', {
        'orders_count': orders_count
    })

@user_passes_test(lambda u: u.role in ['ADMIN', 'WAITER'])
def waiter_dashboard(request):
    all_orders = Order.objects.annotate(date_only=TruncDate('created_at')).order_by('-date_only', '-created_at')

    search_query = request.GET.get('search', '')
    if search_query:
        all_orders = all_orders.filter(
            Q(customer__username__icontains=search_query) |
            Q(id__icontains=search_query)
        )

    distinct_dates = all_orders.values_list('date_only', flat=True).distinct()
    paginator = Paginator(distinct_dates, 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if page_obj.object_list:
        current_day = page_obj.object_list[0]
        orders = all_orders.filter(date_only=current_day)
    else:
        current_day = None
        orders = Order.objects.none()

    price_range = request.GET.get('price_range')
    if price_range:
        try:
            min_p = int(price_range)
            max_p = min_p + 50000
            orders = [o for o in orders if min_p <= o.get_total_price < max_p]
        except (ValueError, TypeError):
            pass

    return render(request, 'dashboard.html', {
        'orders': orders,
        'page_obj': page_obj,
        'current_day': current_day,
        'selected_price': price_range,
        'search_query': search_query
    })