from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class Roleclaims(models.Model):
#     id = models.AutoField(db_column='Id', primary_key=True)  
#     roleid = models.ForeignKey('Roles', models.DO_NOTHING, db_column='RoleId')  
#     claimtype = models.TextField(db_column='ClaimType', blank=True, null=True) 
#     claimvalue = models.TextField(db_column='ClaimValue', blank=True, null=True) 

#     class Meta:
#         managed = False
#         db_table = 'RoleClaims'


# class Roles(models.Model):
#     id = models.TextField(db_column='Id', primary_key=True) 
#     name = models.TextField(db_column='Name', blank=True, null=True) 
#     normalizedname = models.TextField(db_column='NormalizedName', unique=True, blank=True, null=True) 
#     concurrencystamp = models.TextField(db_column='ConcurrencyStamp', blank=True, null=True) 
#     descripcion = models.TextField(db_column='Descripcion', blank=True, null=True) 

#     class Meta:
#         managed = False
#         db_table = 'Roles'


# class UserClaims(models.Model):
#     id = models.AutoField(db_column='Id', primary_key=True)  
#     userid =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
#     claimtype = models.TextField(db_column='ClaimType', blank=True, null=True)  
#     claimvalue = models.TextField(db_column='ClaimValue', blank=True, null=True)  

#     class Meta:
#         managed = False
#         db_table = 'UserClaims'


# class UserRoles(models.Model):
#     userid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     roleid = models.ForeignKey(Roles, models.DO_NOTHING, db_column='RoleId')  

#     class Meta:
#         managed = False
#         db_table = 'UserRoles'


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
    phonenumber = models.TextField(db_column='PhoneNumber', blank=True, null=True)
    state =  models.TextField(db_column='State')
    municipality = models.TextField(db_column='Municipality')
    first_name = models.TextField(db_column='FirstName', blank=True, null=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.username}"

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)


# class Comics(models.Model):
#     id = models.AutoField(db_column='Id', primary_key=True)  
#     nombre = models.TextField(db_column='Nombre')  
#     rutaimagen = models.TextField(db_column='RutaImagen')  
#     usuariovendedorid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     vendedorid = models.TextField(db_column='VendedorId')  

#     class Meta:
#         managed = False
#         db_table = 'Comics'


# class Mensajes(models.Model):
#     id = models.AutoField(db_column='Id', primary_key=True)  
#     emisor = models.IntegerField(db_column='Emisor')  
#     remitente = models.IntegerField(db_column='Remitente')  
#     fechaemision = models.TextField(db_column='FechaEmision')  
#     visto = models.IntegerField(db_column='Visto')  

#     class Meta:
#         managed = False
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
#         managed = False
#         db_table = 'Ofertas'


# class Efmigrationshistory(models.Model):
#     migrationid = models.TextField(db_column='MigrationId', primary_key=True)  
#     productversion = models.TextField(db_column='ProductVersion')  

#     class Meta:
#         managed = False
#         db_table = '__EFMigrationsHistory'


# class Efmigrationslock(models.Model):
#     id = models.AutoField(db_column='Id', primary_key=True)  
#     timestamp = models.TextField(db_column='Timestamp')  

#     class Meta:
#         managed = False
#         db_table = '__EFMigrationsLock'
