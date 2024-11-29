"""
URL configuration for trueque project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.temp_home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register_view, name='register'),
    path('comic/<int:comic_id>/', views.comic_detail, name='comic_detail'),
    path('my-comics/', views.my_comics, name='my_comics'),
    path('comic/add/', views.add_comic, name='add_comic'),
    path('comic/<int:comic_id>/edit/', views.edit_comic, name='edit_comic'),
    path('comic/<int:comic_id>/delete/', views.delete_comic, name='delete_comic'),
    path('comic/<int:comic_id>/offer/', views.make_offer, name='make_offer'),
    path('comic/<int:comic_id>/offer/', views.make_offer, name='make_offer'),
    path('comic/<int:comic_id>/offers/', views.view_offers, name='view_offers'),
]
