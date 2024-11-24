from django.db import models

class Roleclaims(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    roleid = models.ForeignKey('Roles', models.DO_NOTHING, db_column='RoleId')  # Field name made lowercase.
    claimtype = models.TextField(db_column='ClaimType', blank=True, null=True)  # Field name made lowercase.
    claimvalue = models.TextField(db_column='ClaimValue', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AspNetRoleClaims'


class Roles(models.Model):
    id = models.TextField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    normalizedname = models.TextField(db_column='NormalizedName', unique=True, blank=True, null=True)  # Field name made lowercase.
    concurrencystamp = models.TextField(db_column='ConcurrencyStamp', blank=True, null=True)  # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Roles'


class UserClaims(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserId')  # Field name made lowercase.
    claimtype = models.TextField(db_column='ClaimType', blank=True, null=True)  # Field name made lowercase.
    claimvalue = models.TextField(db_column='ClaimValue', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserClaims'


class Userlogins(models.Model):
    loginprovider = models.TextField(db_column='LoginProvider', primary_key=True)  # Field name made lowercase. The composite primary key (LoginProvider, ProviderKey) found, that is not supported. The first column is selected.
    providerkey = models.TextField(db_column='ProviderKey')  # Field name made lowercase.
    providerdisplayname = models.TextField(db_column='ProviderDisplayName', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserLogins'


class UserRoles(models.Model):
    userid = models.OneToOneField('Users', models.DO_NOTHING, db_column='UserId', primary_key=True)  # Field name made lowercase. The composite primary key (UserId, RoleId) found, that is not supported. The first column is selected.
    roleid = models.ForeignKey(Roles, models.DO_NOTHING, db_column='RoleId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserRoles'


class UserTokens(models.Model):
    userid = models.OneToOneField('Users', models.DO_NOTHING, db_column='UserId', primary_key=True)  # Field name made lowercase. The composite primary key (UserId, LoginProvider, Name) found, that is not supported. The first column is selected.
    loginprovider = models.TextField(db_column='LoginProvider')  # Field name made lowercase.
    name = models.TextField(db_column='Name')  # Field name made lowercase.
    value = models.TextField(db_column='Value', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserTokens'


class Users(models.Model):
    id = models.TextField(db_column='Id', primary_key=True)  # Field name made lowercase.
    username = models.TextField(db_column='UserName', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    password = models.TextField(db_column='PasswordHash', blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.TextField(db_column='PhoneNumber', blank=True, null=True)  # Field name made lowercase.
    state =  models.TextField(db_column='State')
    municipality = models.TextField(db_column='Municipality')

    class Meta:
        managed = False
        db_table = 'Users'

    def set_password(self, raw_password):
        """
        Overrides set_password to store the hash in `password`.
        """
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Overrides check_password to validate using `password`.
        """
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)


class Comics(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nombre = models.TextField(db_column='Nombre')  # Field name made lowercase.
    rutaimagen = models.TextField(db_column='RutaImagen')  # Field name made lowercase.
    usuariovendedorid = models.ForeignKey(Users, models.DO_NOTHING, db_column='UsuarioVendedorId', blank=True, null=True)  # Field name made lowercase.
    vendedorid = models.TextField(db_column='VendedorId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Comics'


class Mensajes(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    emisor = models.IntegerField(db_column='Emisor')  # Field name made lowercase.
    remitente = models.IntegerField(db_column='Remitente')  # Field name made lowercase.
    fechaemision = models.TextField(db_column='FechaEmision')  # Field name made lowercase.
    visto = models.IntegerField(db_column='Visto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mensajes'


class Ofertas(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    emisor = models.IntegerField(db_column='Emisor')  # Field name made lowercase.
    remitente = models.IntegerField(db_column='Remitente')  # Field name made lowercase.
    fechaemision = models.TextField(db_column='FechaEmision')  # Field name made lowercase.
    objetotrueque = models.TextField(db_column='ObjetoTrueque')  # Field name made lowercase.
    aceptada = models.IntegerField(db_column='Aceptada')  # Field name made lowercase.
    visto = models.IntegerField(db_column='Visto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ofertas'


class Efmigrationshistory(models.Model):
    migrationid = models.TextField(db_column='MigrationId', primary_key=True)  # Field name made lowercase.
    productversion = models.TextField(db_column='ProductVersion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '__EFMigrationsHistory'


class Efmigrationslock(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    timestamp = models.TextField(db_column='Timestamp')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '__EFMigrationsLock'
