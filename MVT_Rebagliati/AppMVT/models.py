from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager

# CLIENTES

class Clientes (models.Model):
    cuil_cuit = models.CharField(max_length=40)
    nombre_apellido = models.CharField(max_length=40)
    domicilio = models.CharField(max_length=40)
    telefono = models.IntegerField()

    def __str__(self):
        return f"Cuil/Cuit: {self.cuil_cuit}, Nombre: {self.nombre_apellido}, Domicilio: {self.domicilio}, Telefono: {self.telefono}."

# FACTURAS

class Facturas (models.Model):
    fecha = models.DateField()
    tipo = models.CharField(max_length=1)
    nombre_apellido = models.CharField(max_length=40)
    cuil_cuit = models.CharField(max_length=40)
    numero = models.IntegerField()
    monto_sin_iva = models.DecimalField(max_digits=15, decimal_places=2)
    iva = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Fecha: {self.fecha}, Factura: {self.tipo} nº {self.numero}, Nombre: {self.nombre_apellido} Cuil/Cuit: {self.cuil_cuit}, Monto s/Iva: {self.monto_sin_iva}, Iva: {self.iva}."

# PRODUCTOS

class Productos (models.Model):
    code = models.CharField('Codigo', max_length=10, blank= True, null= True)
    producto = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=40)
    precio = models.DecimalField('Precio', max_digits=15, max_length=200, decimal_places=2, blank= True, null= True)
    precio_sin_iva = models.DecimalField(max_digits=15, decimal_places=2)
    iva = models.CharField(max_length=5) 
    imagen = models.ImageField('Imagen del Producto', upload_to='productos/', max_length=200, blank= True, null= True)


    #def __str__(self):
    #    return f"Imagen: {self.imagen}, Producto: {self.producto}, Precio s/iva: {self.precio_sin_iva}, Iva: {self.iva}, Descripcion: {self.descripcion}."

# USUARIOS
class UsuarioManager(BaseUserManager):
    def create_user(self,email,nombres,apellidos,password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico!')
        
        usuario = self.model(
            email = self.normalize_email(email), 
            nombres = nombres, 
            apellidos = apellidos
        )

        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self,email,nombres,apellidos,password):
        usuario = self.create_user(
            email, 
            nombres = nombres, 
            apellidos = apellidos,
            password = password
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario


class Usuario(AbstractBaseUser):
    email = models.EmailField('Correo Electrónico', max_length=254, unique = True)
    nombres = models.CharField('Nombres', max_length=100, blank= False, null= False)
    apellidos = models.CharField('Apellidos', max_length=100, blank= False, null= False)
    imagen = models.ImageField('Imagen de Perfil', upload_to='perfil/', max_length=200, blank= True, null= True)
    usuario_activo = models.BooleanField(default = True)
    usuario_administrador = models.BooleanField(default = False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombres','apellidos','imagen']

    def __str__(self):
        return f'{self.nombres}, {self.apellidos}'

    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador
