from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.db.models import Q,Min,Max

from article.computers.models import *
from article.computers.computer_utils import get_computers_data, get_client_ip, get_location_by_ip, delete_file
from article.computers.file_creater import convertComputerListTotxtFile
from article.orders.models import *
from main.models import *
import json
import time
import random
# Create your views here.

def authentication(request):
    context = {
        "page_title":"connection.ph",
    }
    return render(request,"dashbord-templates/dashbord-connexion.html", context)

def logout(request):
    context = {   
        "page_title":"connection.ph",          
    }
    return render(request,"dashbord-templates/dashbord-connexion.html", context)

def index(request) :
    context = {
        "page_title":"index.ph",
    }
    return render(request,"dashbord-templates/dashbord-index.html", context)

def profile(request) :
    context = {
        "page_title":"profile.ph",
    }
    return render(request,"dashbord-templates/dashbord-userprofile.html", context)

def register(request) :
    context = {
        "page_title":"register.ph",
    }
    return render(request,"dashbord-templates/dashbord-createaccount.html", context)

def supplier(request) :
    context = {
        "page_title":"supplier.ph",
    }
    return render(request,"dashbord-templates/dashbord-addsupplier.html", context)

def computer_list(request) :
    context = {
        "page_title":"computer-list.ph",
    }
    return render(request,"dashbord-templates/dashbord-addcomputer.html", context)

def add_computer_photo(request) :
    context = {
        "page_title":"add-computer-photo.ph",
    }
    return render(request,"dashbord-templates/dashbord-addcomputerphoto.html", context)

def add_computer(request) :
    context = {
        "page_title":"add-computer.ph",
    }
    return render(request,"dashbord-templates/dashbord-addcomputer.html", context)

def processed_orders(request) :
    context = {
        "page_title":"processed-orders.ph",
    }
    return render(request,"dashbord-templates/dashbord-processedorders.html", context)

def unproccessedorders(request) :
    context = {
        "page_title":"unproccessedorders.ph",
    }
    return render(request,"dashbord-templates/dashbord-unproccessedorders.html", context)