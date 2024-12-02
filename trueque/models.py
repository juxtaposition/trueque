from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# class Roleclaims(models.Model):
#     id = models.AutoField(db_column='Id', primary_key=True)  
#     roleid = models.ForeignKey('Roles', models.DO_NOTHING, db_column='RoleId')  
#     claimtype = models.TextField(db_column='ClaimType', blank=True, null=True) 
#     claimvalue = models.TextField(db_column='ClaimValue', blank=True, null=True) 

#     class Meta:
#         db_table = 'RoleClaims'


# class Roles(models.Model):
#     id = models.TextField(db_column='Id', primary_key=True) 
#     name = models.TextField(db_column='Name', blank=True, null=True) 
#     normalizedname = models.TextField(db_column='NormalizedName', unique=True, blank=True, null=True) 
#     concurrencystamp = models.TextField(db_column='ConcurrencyStamp', blank=True, null=True) 
#     descripcion = models.TextField(db_column='Descripcion', blank=True, null=True) 

#     class Meta:
#         db_table = 'Roles'


# class UserClaims(models.Model):
#     id = models.AutoField(db_column='Id', primary_key=True)  
#     userid =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
#     claimtype = models.TextField(db_column='ClaimType', blank=True, null=True)  
#     claimvalue = models.TextField(db_column='ClaimValue', blank=True, null=True)  

#     class Meta:
#         db_table = 'UserClaims'


# class UserRoles(models.Model):
#     userid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     roleid = models.ForeignKey(Roles, models.DO_NOTHING, db_column='RoleId')  

#     class Meta:
#         db_table = 'UserRoles'

#validador personalizado para el número telefónico
phone_regex = RegexValidator(
    regex=r'^\d{10}$',
    message="El número de teléfono debe ser de exactamente 10 dígitos numéricos."
)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


class CustomUsers(AbstractBaseUser, PermissionsMixin):
    username = models.TextField(db_column='UserName', unique=True, blank=True, null=True)
    email = models.TextField(db_column='Email', blank=True, null=True)
    password = models.TextField(db_column='PasswordHash', blank=True, null=True)
    phonenumber = models.CharField(  # Cambiamos a CharField para mejor manejo de la validación
        db_column='PhoneNumber',
        max_length=10,
        blank=True,
        null=True,
        validators=[phone_regex]
    )
    state = models.TextField(db_column='State')
    municipality = models.TextField(db_column='Municipality')
    first_name = models.TextField(db_column='FirstName', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_name = models.TextField(db_column='LastName', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.username}"



class Comic(models.Model):
    STATUS_CHOICES = [
        ('Sin Ofertas Activas', 'Sin Ofertas Activas'),
        ('Trueque en Progreso', 'Trueque en Progreso'),
        ('Con Ofertas Activas', 'Con Ofertas Activas'),
        ('Trueque Finalizado', 'Trueque Finalizado'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='comics/', null=True, blank=True)  # Permitir nulos temporalmente
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comics')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Sin Ofertas Activas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Offer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('accepted', 'Aceptada'),
        ('rejected', 'Rechazada'),
    ]

    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name='offers')
    offerer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offers_made')
    description = models.TextField()
    offered_item = models.CharField(max_length=200)
    offered_item_image = models.ImageField(upload_to='offers/', null=True, blank=True)  # Campo nuevo para la imagen
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Oferta para {self.comic.title} por {self.offerer.username}"


# class Comics(models.Model):
#     id = models.AutoField(db_column='Id', primary_key=True)  
#     nombre = models.TextField(db_column='Nombre')  
#     rutaimagen = models.TextField(db_column='RutaImagen')  
#     usuariovendedorid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     vendedorid = models.TextField(db_column='VendedorId')  

#     class Meta:
#         db_table = 'Comics'


# class Mensajes(models.Model):
#     id = models.AutoField(db_column='Id', primary_key=True)  
#     emisor = models.IntegerField(db_column='Emisor')  
#     remitente = models.IntegerField(db_column='Remitente')  
#     fechaemision = models.TextField(db_column='FechaEmision')  
#     visto = models.IntegerField(db_column='Visto')  

#     class Meta:
#         db_table = 'Mensajes'


# class Ofertas(models.Model):
#     id = models.AutoField(db_column='Id', primary_key=True)  
#     emisor = models.IntegerField(db_column='Emisor')
#     remitente = models.IntegerField(db_column='Remitente')  
#     fechaemision = models.TextField(db_column='FechaEmision')  
#     objetotrueque = models.TextField(db_column='ObjetoTrueque')  
#     aceptada = models.IntegerField(db_column='Aceptada')  
#     visto = models.IntegerField(db_column='Visto')  

#     class Meta:
#         db_table = 'Ofertas'
