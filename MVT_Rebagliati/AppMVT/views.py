from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from AppMVT.forms import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from AppMVT.models import *
from django.views.generic import CreateView


# Create your views here.
def index (request):
    #if request.user.is_authenticated:
    #    return redirect("/AppMVT/home/")
    #else:
    #    return render(request, "index.html")
    return render(request, "index.html")

def home (request):
    return render(request, "home.html")

#LOGINS

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            print("aca11")# debugeee
            user = authenticate(username = user, password = pwd)

            if user is not None:
                login(request, user)
                #return render(request, 'home.html')
                print("aca")# debugeee
                return redirect("/AppMVT/")
            else:
                print("aca2")# debugeee
                return render(request, "login.html", {'form':form})
                return redirect("/AppMVT/login/", {'form':form})
        else:
            print("aca3")# debugeee
            return render(request, "login.html", {'form':form})
            return redirect("/AppMVT/login/", {'form':form})
    form = AuthenticationForm()
    print("aca12")# debugeee
    return render(request, 'login.html', {'form': form})
    return redirect("/AppMVT/login/", {'form':form})

def login_request_model(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            user = authenticate(username = user, password = pwd)

            if user is not None:
                login(request, user)
                return redirect("/AppMVT/")
            else:
                return render(request, "login_model.html", {'form':form})
        else:
            return render(request, "login_model.html", {'form':form})
    form = AuthenticationForm()
    return render(request, 'login_model.html', {'form': form})

def registro(request):
    #form = User_RegisterForm(request.POST)
    form = FormularioUsuario(request.POST, request.FILES)
    if request.method == 'POST':

        if form.is_valid():
            #username = form.cleaned_data["username"]
            #usuario = Usuario(email = request.POST['email'], nombres = request.POST['nombres'], apellidos = request.POST['apellidos'], password = request.POST['password'], imagen = request.FILES['imagen'])
            #usuario.save()
            form.save()
            print("aca4")# debugeee
            return redirect("/AppMVT/")
        else:#decidi regresar el formulario con error
            print("aca5")# debugeee
            return render(request, "usuariosCRUD/registrar_usuario.html", {'form': form})

    form = FormularioUsuario()
    #form = User_RegisterForm()
    return render(request, "usuariosCRUD/registrar_usuario.html", {'form': form})

class RegistrarUsuario(CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name: 'registro.html'

@login_required
def logout_view(request):
    logout(request)
    return redirect("/AppMVT/")

@login_required
def editar_usuario(request):
    usuario = request.user
    user_basic_info = Usuario.objects.get(id = usuario.id)
    form = UserEditForm(request.POST, instance=usuario)
    if request.method == 'POST':
        
        if form.is_valid:
            informacion = form.cleaned_data.get

            user_basic_info.nombres = informacion('nombres')
            user_basic_info.apellidos = informacion('apellidos')
            user_basic_info.password1 = informacion('password1')
            user_basic_info.password2 = informacion('password1')
            user_basic_info.save

            return redirect("/AppMVT/home/")
    else:
        formulario = UserEditForm(initial={'email':usuario.email})
    return render(request, "usuariosCRUD/editar_usuario.html", {"formulario":formulario, "usuario":usuario})

@login_required
def read_usuarios (request=None):
    usuarios = Usuario.objects.all()
    return render(request, "usuariosCRUD/read_usuarios.html", {"usuarios":usuarios})

@login_required
def buscar_usuario (request):
    if request.GET['nombres']:
        nombres = request.GET['nombres']
        busc_usuarios = Usuario.objects.filter(nombres__icontains = nombres)
        return render(request, "usuariosCRUD/read_clientes.html", {"busc_usuarios":busc_usuarios})
    else:
        respuesta= "Introduce el nombre"
    return HttpResponse(respuesta)

@login_required
def delete_usuario (request, usuario_id):
    usuario = Usuario.objects.get(id= usuario_id)
    usuario.delete()
    return redirect('/AppMVT/usuarios')

#CLIENTES

@login_required
def buscar_cliente (request):
    if request.GET['cuil_cuit']:
        cuil_cuit = request.GET['cuil_cuit']
        busc_clientes = Clientes.objects.filter(cuil_cuit__icontains = cuil_cuit)
        return render(request, "clientesCRUD/read_clientes.html", {"busc_clientes":busc_clientes})
    else:
        respuesta= "Introduce el Cuil/Cuit"
    return HttpResponse(respuesta)

@login_required
def read_clientes (request=None):
    clientes = Clientes.objects.all()
    return render(request, "clientesCRUD/read_clientes.html", {"clientes":clientes})

@login_required
def delete_cliente (request, cliente_id):
    cliente = Clientes.objects.get(id= cliente_id)
    cliente.delete()
    return redirect('/AppMVT/clientes')

    #clientes = Clientes.objects.all() #Devuelve toda la lista de clientes
    #return render(request, "clientesCRUD/read_clientes.html", {"clientes":clientes})

    #return render(request, "clientesCRUD/delete_cliente.html")

@login_required
def update_cliente (request, cliente_id):
    cliente = Clientes.objects.get(id = cliente_id)

    if request.method == 'POST':
        formulario = form_clientes(request.POST)

        if formulario.is_valid():
            informacion = formulario.cleaned_data
            cliente.cuil_cuit = informacion['cuil_cuit']
            cliente.nombre_apellido = informacion['nombre_apellido']
            cliente.domicilio = informacion['domicilio']
            cliente.telefono = informacion['telefono']
            cliente.save()
            return redirect('/AppMVT/clientes')

            #clientes = Clientes.objects.all() #Devuelve toda la lista de clientes
            #return render(request, "clientesCRUD/read_clientes.html", {"clientes":clientes})
    else:
        formulario = form_clientes(initial={'cuil_cuit': cliente.cuil_cuit, 'nombre_apellido': cliente.nombre_apellido, 'domicilio': cliente.domicilio, 'telefono': cliente.telefono})
    
    return render(request, "clientesCRUD/update_cliente.html", {"formulario":formulario})

@login_required
def create_cliente (request):
    if request.method == 'POST':
        cliente = Clientes(cuil_cuit = request.POST['cuil_cuit'], nombre_apellido = request.POST['nombre_apellido'], domicilio = request.POST['domicilio'], telefono = request.POST['telefono'])
        cliente.save()
        return redirect('/AppMVT/clientes')

        #clientes = Clientes.objects.all() #Devuelve toda la lista de clientes
        #return render(request, "clientesCRUD/read_clientes.html", {"clientes":clientes})

    return render(request, "clientesCRUD/create_cliente.html")

#FACTURAS

@login_required
def buscar_factura (request):
    if request.GET['numero']:
        numero = request.GET['numero']
        busc_facturas = Facturas.objects.filter(numero__icontains = numero)
        return render(request, "facturasCRUD/read_facturas.html", {"busc_facturas":busc_facturas})
    else:
        respuesta= "Introduce el nº de factura"
    return HttpResponse(respuesta)

@login_required
def read_facturas (request=None):
    facturas = Facturas.objects.all()
    return render(request, "facturasCRUD/read_facturas.html", {"facturas":facturas})

@login_required
def delete_factura (request, factura_id):
    factura = Facturas.objects.get(id= factura_id)
    factura.delete()
    return redirect('/AppMVT/facturas')

@login_required
def create_factura (request):
    if request.method == 'POST':
        factura = Facturas(fecha = request.POST['fecha'], tipo = request.POST['tipo'], nombre_apellido = request.POST['nombre_apellido'], cuil_cuit = request.POST['cuil_cuit'], numero = request.POST['numero'], monto_sin_iva = request.POST['monto_sin_iva'], iva = request.POST['iva'])
        factura.save()
        return redirect('/AppMVT/facturas')

    return render(request, "facturasCRUD/create_factura.html")

#PRODUCTOS

@login_required
def buscar_producto (request):
    if request.GET['producto']:
        producto = request.GET['producto']
        busc_productos = Productos.objects.filter(producto__icontains = producto)
        return render(request, "productosCRUD/read_productos.html", {"busc_productos":busc_productos})
    else:
        respuesta= "Introduce el nombre del producto"
    return HttpResponse(respuesta)

@login_required
def read_productos (request=None):
    productos = Productos.objects.all()
    return render(request, "productosCRUD/read_productos.html", {"productos":productos})

@login_required
def read_productos_clientes (request=None):
    productos = Productos.objects.all()
    return render(request, "productosCRUD/read_productos_clientes.html", {"productos":productos})

@login_required
def buscar_producto_clientes (request):
    if request.GET['producto']:
        producto = request.GET['producto']
        busc_productos = Productos.objects.filter(producto__icontains = producto)
        return render(request, "productosCRUD/read_productos_clientes.html", {"busc_productos":busc_productos})
    else:
        respuesta= "Introduce el nombre del producto"
    return HttpResponse(respuesta)

@login_required
def delete_producto (request, producto_id):
    producto = Productos.objects.get(id= producto_id)
    producto.delete()
    return redirect('/AppMVT/productos/')
  
@login_required  
def update_producto (request, producto_id):
    producto = Productos.objects.get(id = producto_id)

    if request.method == 'POST':
        formulario = form_productos(request.POST)

        if formulario.is_valid():
            informacion = formulario.cleaned_data
            producto.codigo = informacion['codigo']
            producto.producto = informacion['producto']
            producto.descripcion = informacion['descripcion']
            producto.precio = informacion['precio']
            producto.precio_sin_iva = informacion['precio_sin_iva']
            producto.iva = informacion['iva']
            producto.imagen = informacion['imagen']
            producto.save()
            return redirect('/AppMVT/productos/')

    else:
        formulario = form_productos(initial={'codigo': producto.codigo, 'producto': producto.producto, 'descripcion': producto.descripcion, 'precio': producto.precio, 'precio_sin_iva': producto.precio_sin_iva, 'iva': producto.iva, 'imagen': producto.imagen})
    
    return render(request, "productosCRUD/update_producto.html", {"formulario":formulario})

@login_required
def create_producto (request):
    if request.method == 'POST':
        form = form_productos(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            producto = Productos(code = request.POST['code'], producto = request.POST['producto'], descripcion = request.POST['descripcion'], precio = request.POST['precio'], precio_sin_iva = request.POST['precio_sin_iva'], iva = request.POST['iva'], imagen = request.FILES['imagen'])
            producto.save()
            print("aca3")
            return redirect('/AppMVT/productos/')
        else:
            print("aca4")
            return render(request, "productosCRUD/create_producto.html", {'form': form})
    form = form_productos()
    print("aca5")
    return render(request, "productosCRUD/create_producto.html",{'form': form})
    #form = User_RegisterForm(request.POST)
    #form = FormularioUsuario(request.POST)
    #if request.method == 'POST':
    #    if form.is_valid():
    #        #username = form.cleaned_data["username"]
    #        form.save()
    #        print("aca4")# debugeee
    #        return redirect("/AppMVT/")
    #    else:#decidi regresar el formulario con error
    #        print("aca5")# debugeee
    #        return render(request, "registro.html", {'form': form})
    #   
    #form = FormularioUsuario()
    ##form = User_RegisterForm()
    #return render(request, "registro.html", {'form': form})