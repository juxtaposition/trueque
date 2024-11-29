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
                'description': 'La primera aparición de Superman. Esta es una reimpresión conmemorativa en excelente estado. El cómic que dio inicio a la Edad de Oro de los cómics y definió el género de superhéroes. Portada icónica de Superman levantando un auto.',
                'image': 'img/comic-placeholder/v5_8.png',
                'location': 'Polanco, Ciudad de México',
                'offers_count': 25,
                'status': 'available',
                'publisher': 'DC Comics',
                'year': '1938 (Reimpresión)',
                'condition': 'Excelente'
            },
            2: {
                'id': 2,
                'title': 'The Walking Dead - Volumen Compendio 1',
                'description': 'El primer compendio que recopila los números #1-48. Sigue la historia de Rick Grimes y un grupo de sobrevivientes en un mundo post-apocalíptico zombie. Incluye los arcos argumentales más icónicos de la serie.',
                'image': 'img/comic-placeholder/v5_13.png',
                'location': 'Zapopan, Jalisco',
                'offers_count': 15,
                'status': 'available',
                'publisher': 'Image Comics',
                'year': '2009',
                'condition': 'Muy bueno'
            },
            3: {
                'id': 3,
                'title': 'Wolverine - Edición Limitada Old Man Logan',
                'description': 'La aclamada historia de Mark Millar y Steve McNiven. Situada en un futuro distópico donde los villanos han ganado y Logan vive una vida pacífica, hasta que un último viaje lo obliga a desenvainar sus garras una vez más.',
                'image': 'img/comic-placeholder/v5_11.png',
                'location': 'San Pedro Garza García, Nuevo León',
                'offers_count': 18,
                'status': 'available',
                'publisher': 'Marvel Comics',
                'year': '2008',
                'condition': 'Como nuevo'
            },
            4: {
                'id': 4,
                'title': 'The Amazing Spider-Man #300',
                'description': 'Primera aparición completa de Venom. Un número histórico que marca el debut de uno de los villanos más icónicos de Spider-Man. Arte por Todd McFarlane. Este ejemplar está en excelente estado y es muy buscado por coleccionistas.',
                'image': 'img/comic-placeholder/v5_24.png',
                'location': 'Coyoacán, Ciudad de México',
                'offers_count': 30,
                'status': 'available',
                'publisher': 'Marvel Comics',
                'year': '1988',
                'condition': 'Muy bueno'
            },
            5: {
                'id': 5,
                'title': 'Demon Slayer #1',
                'description': 'Primer tomo del manga que se convirtió en un fenómeno global. Sigue la historia de Tanjiro Kamado en su búsqueda por convertir a su hermana nuevamente en humana y vengarse de los demonios. Edición en español.',
                'image': 'img/comic-placeholder/v5_15.png',
                'location': 'Tlalpan, Ciudad de México',
                'offers_count': 12,
                'status': 'available',
                'publisher': 'Panini Manga',
                'year': '2020',
                'condition': 'Excelente'
            },
            6: {
                'id': 6,
                'title': 'Naruto Manga Tomo 1',
                'description': 'El comienzo de una de las series manga más populares de todos los tiempos. Primera edición en español del manga que introdujo al mundo ninja de Naruto Uzumaki. Incluye los primeros capítulos de la serie.',
                'image': 'img/comic-placeholder/v5_18.png',
                'location': 'Guadalajara Centro, Jalisco',
                'offers_count': 8,
                'status': 'available',
                'publisher': 'Panini Manga',
                'year': '2006',
                'condition': 'Bueno'
            },
            7: {
                'id': 7,
                'title': 'The Boys Vol. 1: The Name of the Game',
                'description': 'El cómic que inspiró la serie de Amazon. Una historia oscura y satírica sobre un grupo de vigilantes que mantienen a los superhéroes bajo control. Contenido para adultos.',
                'image': 'img/comic-placeholder/v5_19.png',
                'location': 'Roma Norte, Ciudad de México',
                'offers_count': 20,
                'status': 'available',
                'publisher': 'Dynamite Entertainment',
                'year': '2007',
                'condition': 'Como nuevo'
            },
            8: {
                'id': 8,
                'title': 'Marvel Must-Have: Civil War',
                'description': 'La épica saga completa de Civil War. Incluye la serie principal que enfrentó a Iron Man contra el Capitán América en una batalla ideológica que dividió al universo Marvel. Edición especial Must-Have.',
                'image': 'img/comic-placeholder/v5_20.png',
                'location': 'Santa Fe, Ciudad de México',
                'offers_count': 22,
                'status': 'available',
                'publisher': 'Marvel Comics',
                'year': '2019',
                'condition': 'Excelente'
            },
            9: {
                'id': 9,
                'title': 'DCeased: War of the Undead Gods',
                'description': 'La última entrega de la aclamada serie DCeased. Una historia apocalíptica que lleva la infección tecnológica a escala cósmica. Incluye todos los números de la serie limitada.',
                'image': 'img/comic-placeholder/v5_21.png',
                'location': 'San Nicolás de los Garza, Nuevo León',
                'offers_count': 15,
                'status': 'available',
                'publisher': 'DC Comics',
                'year': '2022',
                'condition': 'Como nuevo'
            },
            10: {
                'id': 10,
                'title': 'The Umbrella Academy Volume 2: Dallas',
                'description': 'El segundo volumen de la serie creada por Gerard Way. Continúa las aventuras de la disfuncional familia de superhéroes mientras intentan prevenir otro apocalipsis. Edición en tapa dura.',
                'image': 'img/comic-placeholder/v5_22.png',
                'location': 'Condesa, Ciudad de México',
                'offers_count': 17,
                'status': 'available',
                'publisher': 'Dark Horse Comics',
                'year': '2009',
                'condition': 'Muy bueno'
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
    if request.method == 'POST':
        comic = get_object_or_404(Comic, id=comic_id)

        # Crear una nueva oferta
        offer = Offer(
            comic=comic,
            offerer=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            image=request.FILES.get('image')
        )
        offer.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)


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


@login_required
def view_offers(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)
    offers = Offer.objects.filter(comic=comic)
    return render(request, 'offers.html', {
        'comic': comic,
        'offers': offers
    })