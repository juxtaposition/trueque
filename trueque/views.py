from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm, CustomUserCreationForm

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('home') 
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def temp_home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {
            'username': request.user,
        })
    else:
        return redirect('login')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def comic_detail(request, comic_id):
    return render(request, 'comic_detail.html', {
        'username': request.user,
    })

@login_required
def my_comics(request):
    comics = [
        {
            'id': 1,
            'title': 'Marvel Zombies Omnibus',
            'description': 'Edición integral de Marvel Zombies, un imperdible para los fans del apocalipsis y los superhéroes. Apenas lo hojeé.',
            'image': 'img/comic-placeholder/v5_8.png',
            'status': 'Sin Ofertas Activas',
        },
        {
            'id': 2,
            'title': 'Naruto n.º 01',
            'description': 'Primer tomo de Naruto. Busco Ternurines.',
            'image': 'img/comic-placeholder/v5_11.png',
            'status': 'Trueque en Progreso',
        },
        {
            'id': 3,
            'title': 'Doraemon Y Los Dioses Del Viento',
            'description': 'Aburrido, algo maltratado (algunas hojas sueltas, pero completo), lo cambio por cualquier otro comic.',
            'image': 'img/comic-placeholder/v5_8.png',
            'status': '20 Ofertas Activas',
        },
        {
            'id': 4,
            'title': 'Dragon Ball Super, Vol. 1',
            'description': 'Primer volumen de Dragon Ball Super, como nuevo.',
            'image': 'img/comic-placeholder/v5_11.png',
            'status': 'Trueque Finalizado',
        }
    ]
    return render(request, 'my_comics.html', {'comics': comics})
