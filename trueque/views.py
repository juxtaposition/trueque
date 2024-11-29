from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomAuthenticationForm, CustomUserCreationForm, ComicForm, OfferForm
from .models import Comic, Offer


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
    try:
        comic = Comic.objects.get(id=comic_id)
    except:
        # Datos de ejemplo para desarrollo
        example_comics = {
            1: {
                'id': 1,
                'title': 'Action Comics #1 Primera Edición',
                'description': 'Edición Especial en buen estado. Busco cómics de primera edición. Estoy abierto a ofertas. Solo gente seria.',
                'image': 'img/comic-placeholder/v5_8.png',
                'location': 'Ecatepec, Estado de México',
                'offers_count': 15,
                'status': 'available'
            },
            2: {
                'id': 2,
                'title': 'The Walking Dead',
                'description': 'Excelente estado, edición especial. Acepto ofertas.',
                'image': 'img/comic-placeholder/v5_13.png',
                'location': 'Ciudad de México',
                'offers_count': 8,
                'status': 'available'
            },
            3: {
                'id': 3,
                'title': 'Wolverine',
                'description': 'Edición limitada de Wolverine. Busco intercambio por otros cómics de X-Men.',
                'image': 'img/comic-placeholder/v5_11.png',
                'location': 'Guadalajara, Jalisco',
                'offers_count': 12,
                'status': 'available'
            },
            4: {
                'id': 4,
                'title': 'Spiderman',
                'description': 'Amazing Spider-Man #1. En perfecto estado.',
                'image': 'img/comic-placeholder/v5_24.png',
                'location': 'Monterrey, Nuevo León',
                'offers_count': 20,
                'status': 'available'
            }
        }

        comic = example_comics.get(comic_id)
        if comic is None:
            # Si no existe ni en la base de datos ni en los ejemplos
            return render(request, '404.html', status=404)

    return render(request, 'comic_detail.html', {
        'comic': comic,
        'username': request.user,
    })


@login_required
def add_comic(request):
    if request.method == 'POST':
        form = ComicForm(request.POST, request.FILES)
        if form.is_valid():
            comic = form.save(commit=False)
            comic.owner = request.user
            comic.save()
            return redirect('my_comics')
    else:
        form = ComicForm()
    return JsonResponse({'form': form.as_p()})

@login_required
def edit_comic(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id, owner=request.user)
    if request.method == 'POST':
        form = ComicForm(request.POST, request.FILES, instance=comic)
        if form.is_valid():
            form.save()
            return redirect('my_comics')
    else:
        form = ComicForm(instance=comic)
    return JsonResponse({'form': form.as_p()})

@login_required
def delete_comic(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id, owner=request.user)
    if request.method == 'POST':
        comic.delete()
        return redirect('my_comics')
    return redirect('my_comics')

@login_required
def make_offer(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.comic = comic
            offer.offerer = request.user
            offer.save()
            return redirect('comic_detail', comic_id=comic_id)
    else:
        form = OfferForm()
    return JsonResponse({'form': form.as_p()})


@login_required
def my_comics(request):
    # Intenta obtener los cómics de la base de datos
    try:
        comics = Comic.objects.filter(owner=request.user)
        if not comics.exists():  # Si no hay cómics en la base de datos, usa los datos de ejemplo
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
    except:
        # Si el modelo Comic aún no existe o hay algún error, usa los datos de ejemplo
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


