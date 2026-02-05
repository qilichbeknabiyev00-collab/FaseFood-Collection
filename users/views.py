# users/views.py (yoki order/views.py)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login
from .forms import RegisterForm,UserEditForm
from .models import User

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dish_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'

@user_passes_test(is_admin)
def user_management_view(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'user_management.html', {'users': users})


@user_passes_test(is_admin)
def edit_user(request, user_id):
    user_to_edit = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    else:
        form = UserEditForm(instance=user_to_edit)
    return render(request, 'edit_user.html', {'form': form, 'edit_user': user_to_edit})


