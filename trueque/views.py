from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
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
        comics_db = Comic.objects.filter(
            Q(status="Sin Ofertas Activas") | Q(status="Con Ofertas Activas") | Q(status="Trueque en Progreso") 
        ).exclude(
            Q(status="Trueque Finalizado")
        ).exclude(
            owner=request.user
        ).order_by('-created_at')[:10]

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
    except Exception as e:
        print(f"error {e}")
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
            # Mejorar los logs de depuración
            print("=" * 50)
            print("DEBUG: Recibiendo nueva oferta")
            print(f"FILES: {request.FILES}")
            print(f"POST: {request.POST}")
            print("Nueva oferta recibida")
            print("POST data:", request.POST.dict())
            print("FILES data:", request.FILES)
            image = request.FILES.get('image')
            if image in request.FILES:
                print("Imagen recibida:")
                print("- Nombre:", request.FILES['image'].name)
                print("- Tamaño:", request.FILES['image'].size)
                print("- Tipo:", request.FILES['image'].content_type)
            else:
                print("No se recibió ninguna imagen")
            print("=" * 50)

            # Verificar que los campos requeridos estén presentes
            title = request.POST.get('title')
            description = request.POST.get('description')
            image = request.FILES.get('image')

            if not title or not description:
                return JsonResponse({
                    'status': 'error',
                    'message': 'El título y la descripción son requeridos'
                }, status=400)

            # Obtener o crear el cómic
            comic = Comic.objects.get(id=comic_id)  # Cambiamos filter.first() por get()

            # Verificar permisos
            if comic.owner == request.user:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No puedes hacer una oferta a tu propio cómic'
                }, status=400)

            comic.status="Trueque en Progreso"
            comic.save()

            # Crear la oferta
            try:
                offer = Offer.objects.create(
                    comic=comic,
                    offerer=request.user,
                    description=description,
                    offered_item=title,
                    offered_item_image=image,
                    status='pending'
                )
                print(f"Oferta creada exitosamente. ID: {offer.id}")
                print(
                    f"Ruta de la imagen: {offer.offered_item_image.path if offer.offered_item_image else 'Sin imagen'}")

                return JsonResponse({
                    'status': 'success',
                    'message': 'Oferta creada exitosamente',
                    'offer_id': offer.id,
                    'image_url': offer.offered_item_image.url if offer.offered_item_image else None
                })

            except Exception as e:
                print(f"Error al guardar la oferta: {str(e)}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'Error al guardar la oferta: {str(e)}'
                }, status=400)

        except Comic.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'El cómic no existe'
            }, status=404)

        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Error inesperado: {str(e)}'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Método no permitido'
    }, status=405)

def my_comics(request):
    # Intenta obtener los cómics de la base de datos
    comicsWithOffers = []
    try:
        comics = Comic.objects.filter(owner=request.user, )
        for comic in comics:
            offer = Offer.objects.filter(status="accepted", comic=comic).first()
            print(offer)
            if offer:
                comicsWithOffers.append({
                "id": comic.id,
                "title": comic.title,
                "description": comic.description,
                "status": comic.status,
                "image": comic.image,
                "offerId": offer.id,
                })
            else:
                comicsWithOffers.append({
                "id": comic.id,
                "title": comic.title,
                "description": comic.description,
                "status": comic.status,
                "image": comic.image
                })

        if not comics.exists():  # Si no hay cómics en la base de datos, usa los datos de ejemplo
            return render(request, 'my_comics.html', {'comics': comicsWithOffers })
    except Exception as e:
        return render(request, 'my_comics.html', {'comics': comicsWithOffers})

    return render(request, 'my_comics.html', {'comics': comicsWithOffers})


@login_required
def view_offers(request, comic_id):
    try:
        # Obtener el cómic de la base de datos
        comic = Comic.objects.get(id=comic_id)
        offers = Offer.objects.filter(comic=comic)

        # Debug: Imprimir información de las ofertas
        for offer in offers:
            print(f"Oferta ID: {offer.id}")
            if offer.offered_item_image:
                print(f"Imagen: {offer.offered_item_image.url}")
            else:
                print("No tiene imagen")

    except Comic.DoesNotExist:
        return render(request, '404.html', status=404)

    return render(request, 'offers.html', {
        'comic': comic,
        'offers': offers
    })


@login_required
def all_offers(request):
    received_offers = Offer.objects.filter(comic__owner=request.user)
    sent_offers = Offer.objects.filter(offerer=request.user)

    offers = []
    print("=" * 50)
    print("Debugging ofertas:")

    # Procesar ofertas recibidas
    for offer in received_offers:
        offers.append({
            'id': offer.id,
            'type': 'received',
            'requested_comic': {
                'title': offer.comic.title,
                'image': offer.comic.image.url if offer.comic.image else static('images/comic-placeholder/v5_8.png'),
                'owner': offer.comic.owner.username,
            },
            'offered_comic': {
                'title': offer.offered_item,
                'description': offer.description,
                'image': offer.offered_item_image.url if offer.offered_item_image else static(
                    'images/comic-placeholder/v5_15.png'),
                'owner': offer.offerer.username,
            },
            'date': offer.created_at.strftime('%Y-%m-%d'),
            'status': offer.get_status_display()  # Cambio aquí
        })

    # Procesar ofertas enviadas (mismo cambio)
    for offer in sent_offers:
        offers.append({
            'id': offer.id,
            'type': 'sent',
            'requested_comic': {
                'title': offer.comic.title,
                'image': offer.comic.image.url if offer.comic.image else static('images/comic-placeholder/v5_8.png'),
                'owner': offer.comic.owner.username,
            },
            'offered_comic': {
                'title': offer.offered_item,
                'description': offer.description,
                'image': offer.offered_item_image.url if offer.offered_item_image else static(
                    'images/comic-placeholder/v5_15.png'),
                'owner': request.user.username,
            },
            'date': offer.created_at.strftime('%Y-%m-%d'),
            'status': offer.get_status_display()  # Cambio aquí
        })

    print("=" * 50)
    return render(request, 'all_offers.html', {
        'offers': offers,
        'default_tab': 'received'  # Indica que el tab inicial será "Recibidas"
    })  



@login_required
def handle_offer(request, offer_id):
    if request.method == 'POST':
        offer = get_object_or_404(Offer, id=offer_id)
        action = request.POST.get('action')

        if action == 'accept':
            offer.status = 'accepted'
            offer.comic.status = 'Trueque Finalizado'
            offer.comic.save()
        elif action == 'reject':
            offer.status = 'rejected'

        offer.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=405)

@login_required
def get_offer_by_id(request, offer_id):
    if request.method == 'GET':
        offer = get_object_or_404(Offer, id=offer_id)
        data = {
            "status": offer.status,
            "description": offer.description,
            "offered_item_image": offer.offered_item_image.url,
            "offerer": offer.offerer.username
        }

        return JsonResponse({'status': 'success', 'offer': data })

    return JsonResponse({'status': 'error'}, status=405)