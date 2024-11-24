from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'temp_login.html', {'form': form})


@login_required
def temp_home(request):
    if request.user.is_authenticated:
        return render(request, 'temp_home.html', {
            'username': request.user,
        })
    else:
        return redirect('login')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')
