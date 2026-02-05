from django.contrib.auth import views as auth_views
from order.views import waiter_dashboard
from django.urls import path, include
from users import views as user_views
from django.contrib import admin
from dish.views import dish_list
from order import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html',redirect_authenticated_user=True), name='login'),
    path('menu/', dish_list, name='dish_list'),
    path('dashboard/', views.waiter_dashboard, name='waiter_dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('update-cart/<int:dish_id>/<str:action>/', views.add_to_order, name='add_to_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', user_views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', user_views.edit_user, name='edit_user'),
    path('admin-panel/users/', user_views.user_management_view, name='user_management'),
    path('admin-panel/users/edit/<int:user_id>/', user_views.edit_user, name='edit_user'),
]