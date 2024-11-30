from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomAuthenticationForm, CustomUserCreationForm, ComicForm, OfferForm
from django.core.files.storage import default_storage
from .models import Comic, Offer
import json



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

    try:
        # Intentar obtener cómics de la base de datos
        comics_db = Comic.objects.exclude(owner=request.user).order_by('-created_at')[:10]

        if comics_db.exists():
            # Si hay cómics en la base de datos, usarlos
            comics_list = []
            for comic in comics_db:
                comics_list.append({
                    'id': comic.id,
                    'title': comic.title,
                    'description': comic.description,
                    'image': comic.image.url if comic.image else 'img/comic-placeholder/v5_8.png',
                    'owner': comic.owner.username,
                    'location': f"{comic.owner.municipality}, {comic.owner.state}",
                    'status': comic.status
                })
        else:
            # Si no hay cómics en la base de datos, usar los de ejemplo
            return

        return render(request, 'home.html', {
            'username': request.user,
            'comics': comics_list
        })
    except:
        # Si hay algún error, usar los datos de ejemplo
        return render(request, 'home.html', {
            'username': request.user,
        })

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required
def comic_detail(request, comic_id):
    try:
        # Intentar obtener el cómic de la base de datos
        comic = Comic.objects.get(id=comic_id)
        comic_data = {
            'id': comic.id,
            'title': comic.title,
            'description': comic.description,
            'image': comic.image.url,
            'owner': comic.owner.username,
            'owner_state': comic.owner.state,  # Agregar estado del propietario
            'owner_municipality': comic.owner.municipality,  # Agregar municipio del propietario
            'status': comic.status,
            'offers_count': comic.offers.count() if hasattr(comic, 'offers') else 0
        }
        return render(request, 'comic_detail.html', {
           'comic': comic_data,
           'username': request.user,
         })
    except Comic.DoesNotExist:
        return render(request, '404.html', status=404)

@login_required
def add_comic(request):
    if request.method == 'POST':
        form = ComicForm(request.POST, request.FILES)
        if form.is_valid():
            comic = form.save(commit=False)
            comic.owner = request.user
            comic.save()
            return JsonResponse({
                'success': True, 
                'message': 'Cómic añadido exitosamente'
            })
        else:
            return JsonResponse({
                'success': False, 
                'errors': form.errors
            })
    else:
        form = ComicForm()
        html = render_to_string('form_comic.html', {'form': form}, request=request)
        return JsonResponse({'html': html})


@login_required
def edit_comic(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id, owner=request.user)
    if request.method == 'POST':
        form = ComicForm(request.POST, instance=comic)
        if request.FILES.get('image'):
            uploaded_file = request.FILES['image']
            image = Image.open(uploaded_file)
            image = image.resize((300, 450))  # Resize to 300x300
            temp_file = BytesIO()
            image.save(temp_file, format='JPEG')  # Save to BytesIO
            temp_file.seek(0)
            comic = form.save(commit=False)
            comic.owner = request.user
            comic.image.save(uploaded_file.name, ContentFile(temp_file.read()), save=True)
            comic.save()
            return JsonResponse({'success': True})
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = ComicForm(instance=comic)

    html = render_to_string('form_comic.html', {'form': form}, request=request)
    return JsonResponse({'html': html})


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
        try:
            print("Datos recibidos:", request.POST)  # Para depuración
            print("Archivos recibidos:", request.FILES)  # Para depuración

            # Verificar que los campos requeridos estén presentes
            title = request.POST.get('title')
            description = request.POST.get('description')
            image = request.FILES.get('image')

            if not title or not description:
                return JsonResponse({
                    'status': 'error',
                    'message': 'El título y la descripción son requeridos'
                }, status=400)

            # Verificar si el cómic existe en la base de datos
            comic = Comic.objects.filter(id=comic_id).first()
            if not comic:
                # Crear el cómic si no existe (usando tus datos de ejemplo)
                comic = Comic.objects.create(
                    id=comic_id,
                    title=f"Comic {comic_id}",  # Ajusta según tus necesidades
                    description="Descripción del cómic",
                    owner=request.user,
                    status='available'
                )

            # Crear la oferta con la imagen
            offer = Offer.objects.create(
                comic=comic,
                offerer=request.user,
                description=description,
                offered_item=title,
                offered_item_image=image if image else None,
                status='pending'
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Oferta creada exitosamente',
                'offer_id': offer.id
            })

        except Exception as e:
            print("Error al crear oferta:", str(e))  # Para depuración
            return JsonResponse({
                'status': 'error',
                'message': f'Error al crear la oferta: {str(e)}'
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Método no permitido'
    }, status=405)

def my_comics(request):
    # Intenta obtener los cómics de la base de datos
    try:
        comics = Comic.objects.filter(owner=request.user)
        if not comics.exists():  # Si no hay cómics en la base de datos, usa los datos de ejemplo
            return render(request, 'my_comics.html', {'comics': comics})
    except:
        return render(request, 'my_comics.html', {'comics': comics})

    return render(request, 'my_comics.html', {'comics': comics})


@login_required
def view_offers(request, comic_id):
    try:
        # Obtener el cómic de la base de datos
        comic = Comic.objects.get(id=comic_id)
        offers = Offer.objects.filter(comic=comic)
    except Comic.DoesNotExist:
        # Si no existe en la base de datos, usa los datos de ejemplo
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
            # Más datos de ejemplo aquí
        }

        comic = example_comics.get(comic_id)
        if comic is None:
            # Si tampoco está en los datos de ejemplo, devuelve un 404
            return render(request, '404.html', status=404)

        # Crear ofertas de ejemplo
        offers = [
            {
                'id': 1,
                'title': 'El Demon Slayer Vol. 1',
                'description': 'Tengo el primer tomo de Demon Slayer, está en súper buen estado, lo leí una vez y lo cuidé mucho. Estoy buscando un cómic raro. Si te interesa, mándame mensaje y negociamos.',
                'image': 'img/comic-placeholder/v5_15.png',
                'offerer': 'Juanito541',
                'location': 'Nopaltepec, Estado de México',
                'status': 'pending'
            },
            # Más ofertas de ejemplo aquí
        ]

    return render(request, 'offers.html', {
        'comic': comic,
        'offers': offers
    })


@login_required
def all_offers(request):
    received_offers = Offer.objects.filter(comic__owner=request.user)
    sent_offers = Offer.objects.filter(offerer=request.user)

    offers = []

    # Procesar ofertas recibidas
    for offer in received_offers:
        offers.append({
            'id': offer.id,
            'type': 'received',
            'requested_comic': {
                'title': offer.comic.title,
                'image': offer.comic.image.url if offer.comic.image else 'img/comic-placeholder/v5_8.png',
                'owner': offer.comic.owner.username,
            },
            'offered_comic': {
                'title': offer.offered_item,
                'description': offer.description,
                'image': offer.offered_item_image.url if offer.offered_item_image else 'img/comic-placeholder/v5_15.png',
                'owner': offer.offerer.username,
            },
            'date': offer.created_at.strftime('%Y-%m-%d'),
            'status': offer.status
        })

    # Procesar ofertas enviadas
    for offer in sent_offers:
        offers.append({
            'id': offer.id,
            'type': 'sent',
            'requested_comic': {
                'title': offer.comic.title,
                'image': offer.comic.image.url if offer.comic.image else 'img/comic-placeholder/v5_8.png',
                'owner': offer.comic.owner.username,
            },
            'offered_comic': {
                'title': offer.offered_item,
                'description': offer.description,
                'image': offer.offered_item_image.url if offer.offered_item_image else 'img/comic-placeholder/v5_15.png',
                'owner': request.user.username,
            },
            'date': offer.created_at.strftime('%Y-%m-%d'),
            'status': offer.status
        })

    return render(request, 'all_offers.html', {'offers': offers})


@login_required
def handle_offer(request, offer_id):
    if request.method == 'POST':
        offer = get_object_or_404(Offer, id=offer_id)
        action = request.POST.get('action')

        if action == 'accept':
            offer.status = 'accepted'
            offer.comic.status = 'in_progress'
            offer.comic.save()
        elif action == 'reject':
            offer.status = 'rejected'

        offer.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=405)