from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Rutas principales
    path('', views.temp_home, name='home'),
    path('admin/', admin.site.urls),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Gestión de cómics
    path('my-comics/', views.my_comics, name='my_comics'),
    path('comic/add/', views.add_comic, name='add_comic'),
    path('comic/<int:comic_id>/', views.comic_detail, name='comic_detail'),
    path('comic/<int:comic_id>/edit/', views.edit_comic, name='edit_comic'),
    path('comic/<int:comic_id>/delete/', views.delete_comic, name='delete_comic'),
    
    # Gestión de ofertas
    path('comic/<int:comic_id>/offer/', views.make_offer, name='make_offer'),
    path('comic/<int:comic_id>/offers/', views.view_offers, name='view_offers'),
    path('offers/', views.all_offers, name='all_offers'),
    path('offer/<int:offer_id>/handle/', views.handle_offer, name='handle_offer'),
]

# Agregar las rutas para servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)