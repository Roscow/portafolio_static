from django.db import models


class Articulo(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    recurso = models.CharField(max_length=500)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')
    fecha = models.DateField()

    def __str__(self):
        return self.titulo
    
    class Meta:
        managed = False
        db_table = 'articulo'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cita(models.Model):
    cita_id = models.AutoField(primary_key=True)
    contenido = models.TextField()
    autor = models.CharField(max_length=200)
    fuente = models.CharField(max_length=200)

    def __str__(self):
        return self.contenido
    
    class Meta:
        managed = False
        db_table = 'cita'

class Componente(models.Model):
    descripcion = models.CharField(max_length=2000)
    proyecto = models.ForeignKey('Proyecto', models.DO_NOTHING, db_column='proyecto')
    descripcion_es = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return str(self.proyecto) + "_"+ str(self.descripcion)
    
    class Meta:
        managed = False
        db_table = 'componente'

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Estado(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'estado'


class Estudio(models.Model):
    nombre = models.CharField(max_length=50)
    recurso = models.CharField(max_length=500)
    fecha = models.DateField(blank=True, null=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')
    descripcion = models.CharField(max_length=2000, blank=True, null=True)
    institucion = models.CharField(max_length=200, blank=True, null=True)
    recurso_pdf = models.FileField(upload_to='certificados/',null=True, blank=True)
    recurso_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        managed = False
        db_table = 'estudio'


class Habilidad(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    nivel = models.IntegerField()
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')
    icon_path = models.CharField(max_length=500, blank=True, null=True)
    progreso = models.DecimalField(max_digits=4, decimal_places=2)
    link_roadmap= models.CharField(max_length=1000, blank=True, null=True)
    roadmap_path =  models.CharField(max_length=1000, blank=True, null=True)
    def __str__(self):
        return self.nombre
    
    class Meta:
        managed = False
        db_table = 'habilidad'


class Musica(models.Model):
    cancion = models.CharField(primary_key=True, max_length=255)  # The composite primary key (cancion, artista) found, that is not supported. The first column is selected.
    artista = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'musica'
        unique_together = (('cancion', 'artista'),)


class Proyecto(models.Model):
    nombre = models.CharField(max_length=50)
    fecha = models.DateField()
    recurso = models.CharField(max_length=500)
    imagen = models.ImageField(upload_to='proyectos/')
    imagen2 = models.ImageField(upload_to='proyectos/')
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario')
    descripcion = models.TextField(max_length=2000, blank=True, null=True)
    recurso2 = models.CharField(max_length=2000, blank=True, null=True)
    descripcion_es = models.TextField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        managed = False
        db_table = 'proyecto'
      


class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'usuario'



class Videos(models.Model):
    nombre = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'videos'

class ProyectoHabilidad(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, db_column='proyecto')
    habilidad = models.ForeignKey(Habilidad, models.DO_NOTHING, db_column='habilidad')

    def __str__(self):
        return str(self.proyecto) + "_"+ str(self.habilidad)
    
    class Meta:
        managed = False
        db_table = 'proyecto_habilidad'