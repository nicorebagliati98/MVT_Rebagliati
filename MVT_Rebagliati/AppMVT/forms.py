from tkinter import Widget
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from AppMVT.models import Usuario, Productos


#CLIENTES

class form_clientes (forms.Form):
    cuil_cuit = forms.CharField(max_length=40)
    nombre_apellido = forms.CharField(max_length=40)
    domicilio = forms.CharField(max_length=40)
    telefono = forms.IntegerField()
    
# FACTURAS

class form_facturas (forms.Form):
    fecha = forms.DateField()
    tipo = forms.CharField(max_length=1)
    nombre_apellido = forms.CharField(max_length=40)
    cuil_cuit = forms.CharField(max_length=40)
    numero = forms.IntegerField()
    monto_sin_iva = forms.DecimalField(max_digits=15, decimal_places=2)
    iva = forms.DecimalField(max_digits=15, decimal_places=2)

# PRODUCTOS

class form_productos (forms.Form):
    #class Meta:
    #    model = Productos
    #    fields = '__all__'
    code = forms.CharField(label='Codigo',max_length=10)
    producto = forms.CharField(label='Nombre del producto',max_length=40)
    descripcion = forms.CharField(label='Descripcion',max_length=40)
    precio = forms.DecimalField(label='Precio',max_digits=15, decimal_places=2)
    precio_sin_iva = forms.DecimalField(label='Precio s/iva',max_digits=15, decimal_places=2)
    iva = forms.CharField(label='iva',max_length=5)
    imagen = forms.ImageField(label='Imagen del producto')
    
    class Meta:
        model = Productos
        fields = ['code','producto','descripcion','precio','precio_sin_iva','iva','imagen']
        #saca los mensajes de ayuda
        help_text = {k:"" for k in fields}


# REGISTER
class User_RegisterForm(UserCreationForm):
    username= forms.CharField(label="Nombre de usuario")
    email = forms.EmailField()
    password1= forms.CharField(label="Contraseña", widget= forms.PasswordInput)
    password2= forms.CharField(label="Repetir Contraseña", widget= forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

class FormularioUsuario(forms.ModelForm):
    # Formulario de registro de un usuario en la base de datos
    imagen = forms.ImageField(label='Imagen de Perfil')
    password1 = forms.CharField(label='Contraseña', widget= forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required': 'required'
        }
    ))
    password2 = forms.CharField(label='Verifique su contraseña', widget= forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            'required': 'required'
        }
    ))
    class Meta:
        model = Usuario
        fields = ('email','nombres','apellidos','imagen')
        widget = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Correo Electrónico'
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombres'
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Apellidos'
                }
            )#,
            #'imagen': forms.ImageField(
            #    attrs={
            #        'class': 'form-control',
            #        'placeholder': 'Imagen de Perfil'
            #    }
            #)
        }
    def clean_password2(self):
        # Validación de contraseñas
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden...')
        return password2
    
    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserEditForm(FormularioUsuario):
    nombres = forms.CharField(label="Modificar Nombres")
    apellidos = forms.CharField(label="Modificar Apellidos")
    password1 = forms.CharField(label="Modificar Contraseña")
    password2 = forms.CharField(label="Repetir Contraseña")
    imagen = forms.ImageField(label='Imagen de Perfil')

    class Meta:
        model = Usuario
        fields = ['nombres','apellidos','password1','password2','imagen']
        #saca los mensajes de ayuda
        help_text = {k:"" for k in fields}