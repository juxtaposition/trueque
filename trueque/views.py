from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm

from django.contrib.auth import authenticate, login
from django.contrib import messages

# def login_view(request):
#     if request.method == 'POST':
#         form = CustomAuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = CustomAuthenticationForm()
#     return render(request, 'temp_login.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Logs the user in
            return redirect("home")  # Redirect to a home page or another view
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "temp_login.html")
# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user) 
#             return redirect('home') 
#         else:
#             return render(request, 'temp_register.html', {'form': form})
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'temp_register.html', {'form': form})

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
