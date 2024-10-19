from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.db.models import Q,Min,Max
from .models import *

from zoodoAI.zoodo_model import zoodoAI
from article.computers.models import *
from article.computers.computer_utils import get_computers_data, get_client_ip, get_location_by_ip, delete_file
from article.computers.file_creater import convertComputerListTotxtFile
from article.orders.models import *
from main.models import *
from .computer_utils import recommended_object_builder
import json
import time
import random

def home(request) :
    context = {
        "page_title":"index.ph",
        "brands":Brand.objects.all()
    }
    # result = zoodo_model.model_zoodo(activity_description="software developer", json_computer_data=json_computer_data)
    return render(request,"index.html", context)


recommendations_added = [
        {
            "id": 1,
            "name": "PowerBook Pro X1",
            "price": 1299.99,
            "specs": {
                "ram": "16GB",
                "storage": "512GB SSD",
                "cpu": "Intel Core i7",
                "gpu": "NVIDIA GeForce RTX 3060"
            },
            "images": [ 
                { "src": 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtRdGjFF0ZPhU54xxuTXqU_6ueRxuppnG13wjO1pJ1fRpUO5Qdnyfr7Nr-4flh2nBWdUo&usqp=CAU', "alt": 'Front view of Laptop Model A with screen on' },
                { "src": 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRS0fPvrCz7piwQRplsLoqAxsYvL-dOAS27xe-5f0burHKLwCfg_SxgreMyHkBVcEjjUPM&usqp=CAU', "alt": 'Side view of Laptop Model A showing ports' },
                { "src": 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_qENvolnRfwDlmnkloNP7xlyC0JMA7dFfBQ&s', "alt": 'Laptop Model A keyboard close-up' }
            ],
            "image": "https://m.media-amazon.com/images/I/71CUP80TyEL._AC_SL1500_.jpg",
            "description": "A powerful laptop perfect for professionals and gamers alike."
        },
        {
            "id": 2,
            "name": "UltraSlim 5000",
            "price": 899.99,
            "specs": {
                "ram": "8GB",
                "storage": "256GB SSD",
                "cpu": "AMD Ryzen 5",
                "gpu": "Integrated AMD Radeon Graphics"
            },
            "image": "https://cdn.britannica.com/77/170477-050-1C747EE3/Laptop-computer.jpg",
            "images": [
            { "src": 'https://cdn.britannica.com/77/170477-050-1C747EE3/Laptop-computer.jpg', "alt": 'Front view of Laptop Model A with screen on' },
            { "src": 'https://cdn.britannica.com/77/170477-050-1C747EE3/Laptop-computer.jpg', "alt": 'Side view of Laptop Model A showing ports' },
            { "src": 'https://cdn.britannica.com/77/170477-050-1C747EE3/Laptop-computer.jpg', "alt": 'Laptop Model A keyboard close-up' }
            ],
            "description": "Ultra-portable and perfect for on-the-go productivity."
        },
        {
            "id": 3,
            "name": "CreatorStation Pro",
            "price": 1799.99,
            "specs": {
                "ram": "32GB",
                "storage": "1TB SSD + 2TB HDD",
                "cpu": "Intel Core i9",
                "gpu": "NVIDIA GeForce RTX 3080"
            },
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZXYj_pgsx5Xlwhqzszn9EKRrptoGt9bRtuA&s",
            "images": [
                { "src": 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZXYj_pgsx5Xlwhqzszn9EKRrptoGt9bRtuA&s', "alt": 'Front view of Laptop Model A with screen on' },
                { "src": 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRqR7pi0xDqusODJSn2bH1lLTZypFABKx123A&s', "alt": 'Side view of Laptop Model A showing ports' },
                { "src": 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_O9PkUfg8dBM1RqkBGo_dJG3qGNZJe1-Pfg&s', "alt": 'Laptop Model A keyboard close-up' }
            ],
            "description": "Designed for content creators and 3D artists who need maximum performance."
        }
    ]
def recommendation(request):


    context = {
        "page_title": "recommendation.ph",
        "computer_details":recommendations_added
    }

    return render(request, "recommendation.html", context)

def recommendationForm(request):
    
    context = {
        "tolerances":["50", "60", "80", "100", ],
        "minBudget":Computer.objects.aggregate(Min('price_amount'))['price_amount__min'], # le plus petit budget
        "maxBudget":Computer.objects.aggregate(Max('price_amount'))['price_amount__max'], # le plus petit budget
    }
    return render(request, "recommendation_form_ai.html", context)

def recommendationFormWithoutAI(request):

    context = {
        "page_title":"index.ph",
        "brands":Brand.objects.all(),
        "computerRAMS":Memory.objects.all(),
        "tolerances":["50", "60", "80", "100", ],
        "storages":["2TB SSD", "512 SSD", "1TB SSD", ],
        "speeds":["2GHZ", "1.9 GHZ", "3GHZ"],
        "cores":["core i 3", "core i 5", "core i 7", "core i 9", "core i 11"]
    }
    return render(request, "recommendation_form.html", context)

@require_POST
def contact(request):
    try:
        # Load JSON data from the request body
        data = json.loads(request.body)

        # Extracting data from the request with default values
        name = data.get('name', '')
        email = data.get('email', '')
        subject = data.get('subject', '')
        message = data.get('message', '')

        # Validate input data (optional but recommended)
        if not name or not email or not subject or not message:
            return JsonResponse({"message": "All fields are required."}, status=400)

        # Check if a similar message already exists
        if not userMessage.objects.filter(
            fullname=name,
            email=email,
            subject=subject,
            message=message  
        ).exists():
            # Create a new user message instance
            instance = userMessage.objects.create(
                fullname=name,
                email=email,
                subject=subject,
                message=message   
            )
            instance.save()

            return JsonResponse({"message": "Votre message a été envoyé avec success ! Merci pour votre confiance"}, status=201)
        else:
            return JsonResponse({"message": "Votre message a été envoyé avec success !"}, status=409)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Erreur"}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)


def privacy(request) :
    context = {
        "page_title":"privacies.ph"
    }
    
    return render(request,"privacy.html", context)
def about(request) :
    
    context = {
        "page_title":"about.ph"
    }
    return render(request,"detail.html", context)

def successPage(request):
    context = {}
    return render(request, "page_success.html", context)


def errorPage(request):
    context = {}
    return render(request, "api_444_error.html", context)

def detail(request, id, time) :
    # Information sur l'ordi, raison de la recomm, les photos
    relevant_computer = Computer.objects.filter(id = id).first()
    recommendation_info = RecommendationResult.objects.filter(computer_id = id,recommendation_time = time).first()
    computer_images = ComputerPhoto.objects.filter(computer=relevant_computer)

    # Recuperer tous les details de l'ordinateur
    recommend = recommended_object_builder(relevant_computer, computer_images, recommendation_info)
    context = {
        "page_title":"detail.ph",
        "computer_details":recommend,
        "id_computer":id,
        "time_info":time
    }
    return render(request,"detail.html", context)


from decimal import Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # You can also use str(obj) for higher precision
        return super(DecimalEncoder, self).default(obj)
    
def select_computers(budgetMin, max_price_set):
    # Étape 1: Sélection des ordinateurs des partenaires (max 30)
    partner_comp = Computer.objects.filter(
        price_amount__range=(int(budgetMin), int(max_price_set)), supplier__is_partner=True
    )
    partner_count = partner_comp.count()
    # Limiter le nombre de partenaires à un maximum de 30 de façon aleatoire
    selected_partner_computers = partner_comp.order_by('?')[:min(30, partner_count)]
    # Étape 2: Calcul du nombre restant à sélectionner parmi les non-partenaires
    remaining_to_select = 50 - selected_partner_computers.count()
    # Sélectionner les ordinateurs de non-partenaires pour compléter jusqu'à 50
    if remaining_to_select > 0:
        non_partner_comp = Computer.objects.filter(
            price_amount__range=(int(budgetMin), int(max_price_set)), supplier__is_partner=False
        )
        # Limiter à 'remaining_to_select' ordinateurs non-partenaires de façon aleatoire
        selected_non_partner_computers = non_partner_comp.order_by('?')[:remaining_to_select]
    else:
        selected_non_partner_computers = Computer.objects.none()
    # Étape 3: Combiner les deux QuerySets (partenaires et non-partenaires)
    combined_selection = selected_partner_computers | selected_non_partner_computers
    return combined_selection


@require_http_methods(["GET", "POST"])
def withai_recommendation(request):
    context = {}  
    if request.method == "POST":
        budgetMin = request.POST.get('budgetMin', '0')
        budgetMax = request.POST.get('budgetMax', '0')
        alpha     = request.POST.get('alpha', '0')
        jobTile   = request.POST.get('jobTile', '')
        jobDescription   = request.POST.get('jobDescription', '')
        max_price_set =  (int(budgetMax) * (int(alpha)/100)) + int(budgetMax) 

        # Processus selection des ordinateurs
        relevant_computers = select_computers(budgetMin=budgetMin, max_price_set=max_price_set)

        # Enregistrer les informations sur l'utilisateur qui a fait la req
        user_ip       = get_client_ip(request)
        user_location = get_location_by_ip(user_ip)
        if(len(relevant_computers)== 0):
            context["maxBudget"] = budgetMin
            context["minBudget"] = max_price_set
            
            return render(request, "api_444_error.html", context)

        # Creation d'un fichier txt contenant la liste des ordi pour l'IA
        start_time = time.time()
        data_file_name= f"computers_info_{int(start_time)}.txt" # nom uniq du fichier
        computers_data = get_computers_data(relevant_computers) # Liste des ordi
        isFileCreated  = convertComputerListTotxtFile(computers_data, data_file_name) # conversion
        file_path_error = ""
        computer_recommended = []
        if isFileCreated:
            try:
                        # Utilisation de l'IA
                activity_description = f"{jobTile}" if len(jobDescription)==0 else f"Titre: {jobTile} Petite description à prendre également en compte: {jobDescription}"
                result,global_total_tokens, file_path = zoodoAI(data_file_name = data_file_name,activity_description=activity_description, max_num=15)            
                delete_status = delete_file(file_path) # supprime le fichier temporaire contenant la liste des ordi en text utilisé par l'IA
                file_path_error = file_path
                # Enregister total de tokens generer par l'utilisateur
                token_instance = TokensList(
                            number = global_total_tokens
                )
                token_instance.save()

                # Enregister le result de la recommendation 
                for r in result:
                    recommendation = RecommendationResult(
                        computer_id=r["id"],
                        choose_reason=r["reason"],
                        recommendation_time=start_time,
                        max_budget=max_price_set,
                        min_budget=budgetMin,
                        job_title=jobTile,
                        job_description=jobDescription
                    )
                    recommendation.save()

                    computer_instance = Computer.objects.filter(pk=r["id"]).first()
                    cover_image       = ComputerPhoto.objects.filter(computer=computer_instance, is_cover=True).first()
                    computer_recommended.append({
                            "id": r["id"],
                            "model":computer_instance.model,
                            "time": start_time,
                            "image": cover_image.url,
                            "price": float(computer_instance.price_amount),
                            "color":"black",
                            "processor": f'{computer_instance.processor.model}',
                            "brand":computer_instance.brand.name,
                            "ram": computer_instance.memory.capacity,
                            "storage": "512",
                        })
                            
            except Exception as e :
                delete_status = delete_file(file_path_error) # supprime le fichier temporaire contenant la liste des ordi en text utilisé par l'IA
                return render(request, "api_444_error.html", {"erreur":e})

    return render(request,"recommendation.html", {
                        "recommendation":json.dumps(computer_recommended, cls=DecimalEncoder),
                        "minBudget":budgetMin,
                        "maxBudget":max_price_set,
                        "computerBrands":Brand.objects.all(),
                        "computerColors":ComputerColor.objects.all(),
                        "computerRAMS":Memory.objects.all()
                        })

@require_POST
def withouai_validateStep2(request):
    try:
        # Extraction des données JSON envoyées dans la requête
        data = json.loads(request.body)
        minbudget = data.get("minBudget")
        maxbudget = data.get("maxBudget")
        brand_list = data.get("brand_list", [])  
        
        # Filtrage des ordinateurs en fonction de la gamme de prix
        relevant_computers = Computer.objects.filter(
            price_amount__range=(int(minbudget), int(maxbudget))
        )
        
        if relevant_computers.exists(): # Vérifie si des ordinateurs ont été trouvés
            no_brand = []
            computer_data = []
            
            if brand_list:
                # Filtrer les ordinateurs en fonction des marques sélectionnées
                relevant_computers = relevant_computers.filter(brand__name__in=brand_list)
                relevant_computers_brand = {computer.brand.name for computer in relevant_computers}
                computer_data = [computer.id for computer in relevant_computers]
                
                # Rechercher les marques sélectionnées mais non trouvées dans la gamme de prix
                no_computer_brand_find = set(brand_list).difference(relevant_computers_brand)
                
                if len(no_computer_brand_find)!=0:
                    # Trouver l'ordinateur le moins cher pour les marques non trouvées dans la gamme de prix
                    for brand_name in no_computer_brand_find:
                        computer_brand_find = Computer.objects.filter(
                            brand__name=brand_name
                            ).order_by('price_amount').first()
                        
                        # Extraire les identifiants des ordinateurs trouvés
                        if computer_brand_find:
                            # Ajoute les informations des marques non trouvées avec leur prix le moins cher
                            no_brand.append({"price": computer_brand_find.price_amount, "brand": brand_name})

                    return JsonResponse({
                        "message": "partial success", 
                        "brand_find": list(relevant_computers_brand),
                        "computers": computer_data,"maxbudget":maxbudget,
                        "moreInformations": no_brand, "minbudget":minbudget,
                        "flag":0 # Pemert d'afficher le div pour afficher ces informer
                        }, status=200) 
                    
                # Tous les marques avec un tel prix ont été trouver
                return JsonResponse({"message": "success", "computers": computer_data}, status=200) 
            
        else:
            computer_data = Computer.objects.all().order_by('price_amount').first()
            return JsonResponse({
                "message": "no_data", 
                "cheapest_price": computer_data.price_amount,
                "flag":1 # Permet de fermer le div d'information
            }, status=200)
            
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({"message": str(e)}, status=500)
    

from datetime import datetime, timedelta
@require_POST
def processOrderPage(request):
    try:
        data = json.loads(request.body)
        first_name = data.get('first_name', '')
        last_name  = data.get('last_name', '') 
        phone      = data.get('phone', '00 00 00 00')
        location   = data.get('location', '')
        computer   = data.get('id_computer', '')
        print(request.body)
        # Check if the computer exists
        relevant_computer = Computer.objects.filter(pk=computer).first()
        if not relevant_computer:
            return JsonResponse({"message": "Computer not found"}, status=404)
        
        # Check if the order already exists
        if Commend.objects.filter(first_name=first_name, last_name=last_name, computer=relevant_computer, phone=phone, location=location).exists():
            return JsonResponse({"message": "Order already exists"}, status=200)
        
        # Save the new order
        delivery_date = datetime.now().date() + timedelta(days=3)
        isinstance_order = Commend(
            first_name=first_name,
            last_name=last_name,
            computer=relevant_computer,
            phone=phone,
            location=location,
            delivery_date=delivery_date
        )
        isinstance_order.save()

        return JsonResponse({"message": "Order created successfully"}, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON format"}, status=400)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)