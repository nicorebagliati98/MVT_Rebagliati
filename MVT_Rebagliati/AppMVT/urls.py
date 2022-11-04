from django.urls import path
from AppMVT.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home),
    #path('home/', home),
    #LOGIN
    path('login/', login_request),
    path('login_model/', login_request_model),
    path('logout/', logout_view),
    #USUARIOS
    path('registro/', registro),
    path('editar_usuario/', editar_usuario),
    path('buscar_usuario/', buscar_usuario),
    path('usuarios/', read_usuarios),
    path('delete_usuario/<usuario_id>', delete_usuario),
    #CLIENTES
    path('clientes/', read_clientes),
    path('buscar_cliente/', buscar_cliente),
    path('create_cliente/', create_cliente),
    path('delete_cliente/<cliente_id>', delete_cliente),
    path('update_cliente/<cliente_id>', update_cliente),
    #PRODUCTOS
    path('productos/', read_productos),
    path('buscar_producto/', buscar_producto),
    path('create_producto/', create_producto),
    path('delete_producto/<producto_id>', delete_producto),
    path('update_producto/<producto_id>', update_producto),
    path('productos_clientes/', read_productos_clientes),
    path('buscar_producto_clientes/', buscar_producto_clientes),
    #FACTURAS
    path('facturas/', read_facturas),
    path('buscar_factura/', buscar_factura),
    path('create_factura/', create_factura),
    path('delete_factura/<factura_id>', delete_factura),
]