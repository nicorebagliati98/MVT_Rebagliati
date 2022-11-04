from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from AppMVT.models import *

def inicio(request):
    return HttpResponse("Hola soy la pagina home")

def redirectAppMVT(request):
    return redirect('AppMVT/')

