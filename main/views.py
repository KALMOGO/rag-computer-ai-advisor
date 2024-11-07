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
from .simple_order_utils import *
from django.shortcuts import redirect

import json
import time
import random

def home(request) :
    context = {
        "page_title":"index.ph",
    }
    return render(request,"index.html", context)


def notUrlfind(request):
    return render(request, '404_error.html')


def market(request) :
    budgetMin     = Computer.objects.aggregate(Min('price_amount'))['price_amount__min']
    max_price_set = Computer.objects.aggregate(Max('price_amount'))['price_amount__max']
    computer_recommended = [] 

    # Recupere au maximun 100 ordinateurs de façon aleatoire
    computers = Computer.objects.all().order_by('?')[:100]

    for computer_instance in computers:
        cover_image       = ComputerPhoto.objects.filter(computer=computer_instance, is_cover=True).first()
        computer_recommended.append({
                                "id": computer_instance.id,
                                "model":computer_instance.model,
                                "time": computer_instance.id,
                                "image": cover_image.image.url if cover_image else cover_image.url,
                                "price": float(computer_instance.price_amount),
                                "color":computer_instance.color.color,
                                "processor": f'{computer_instance.processor.model}',
                                "brand":computer_instance.brand.name,
                                "ram": computer_instance.memory.capacity,
                                "storage": computer_instance.storages.first().capacity,
                            })
    return render(request,"market-place.html",  {
                        "recommendation":json.dumps(computer_recommended, cls=DecimalEncoder),
                        "minBudget":budgetMin,
                        "maxBudget":max_price_set,
                        "computerBrands":Brand.objects.all(),
                        "computerColors":ComputerColor.objects.all(),
                        "computerRAMS":Memory.objects.all()
                        })



def recommendationForm(request): # Avec IA
    """
    Return a HTML page with a form containing inputs for budget 
    selection and a tolerance input. The form will be processed by 
    the recommendationFormSubmit view.

    :param request: The HTTP request object.
    :return: A rendered HTML page.
    """
    context = {
        "tolerances":["50", "60", "80", "100", ],
        "minBudget":Computer.objects.aggregate(Min('price_amount'))['price_amount__min'], # le plus petit budget
        "maxBudget":Computer.objects.aggregate(Max('price_amount'))['price_amount__max'], # le plus petit budget
        "page_title":"index.ph",
        "jobs": json.dumps({"list": [job.name for job in ListJob.objects.all()]}, ensure_ascii=True),
    }
    return render(request, "recommendation_form_ai.html", context)

def recommendationFormWithoutAI(request): # Sans IA
    """
    Return a rendered HTML page with a form to filter computers without using AI.
    The page displays a form with the following fields:
        - a dropdown to select the brand
        - a dropdown to select the min and max budget
        - a dropdown to select the min and max tolerance
        - a checkbox list to select the storage
        - a checkbox list to select the speed
        - a checkbox list to select the number of cores
    The form will filter the computers and redirect to the recommendation page with the filtered computers.
    """
    processor_speeds = [processor.base_clock_speed for processor in Processor.objects.all()]
    context = {
        "brands":Brand.objects.all(),
        "computerRAMS":Memory.objects.all(),
        "storages":Storage.objects.all(),
        
        "processor_speeds":  json.dumps(processor_speeds),
        "minBudget":Computer.objects.aggregate(Min('price_amount'))['price_amount__min'],
        "maxBudget":Computer.objects.aggregate(Max('price_amount'))['price_amount__max'],
        "cores":[int(processor.cores - 1) for processor in Processor.objects.all()], # la capacité des procs - 1

        "tolerances":["50", "60", "80", "100", ],
        "page_title":"index.ph",
    }
    return render(request, "recommendation_form.html", context)

@require_POST
def contact(request):
    try:
        # Load JSON data from the request body
        data = json.loads(request.body)

        # Extracting data from the request with default values
        name    = data.get('name', '')
        email   = data.get('email', '')
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
    context = {
  
    }
    return render(request, "page_success.html", context)


def errorPage(request):
    context = {}
    return render(request, "api_444_error.html", context)

def detail(request, id, time) :
    """
    Renders the detail page for a specific computer recommendation.

    This view retrieves detailed information about a computer based on the given
    `id` and `time` parameters. It checks whether the recommendation was made by
    AI or manually by the user. The relevant computer details, images, and 
    accessories are fetched and rendered on the "detail.html" template. If no
    recommendation is found, a 404 error page is displayed.

    :param request: The HTTP request object.
    :param id: The ID of the computer.
    :param time: The timestamp when the recommendation was made.
    :return: A rendered HTML page with computer details or a 404 error page.
    """
    # Information sur l'ordi, raison de la recomm, les photos
    relevant_computer = Computer.objects.filter(id = id).first()
    # Recuperer les photos
    computer_images = ComputerPhoto.objects.filter(computer=relevant_computer)

    # Recuperer les details de l'ordinateur Si c'est l'IA qui a fait la recommandation
    recommendation_info_ai = RecommendationResult.objects.filter(
        computer_id = id,recommendation_time = time).first()
    
    # Recuperer les details de l'ordinateur Si c'est l'utilisateur qui a fait la recommandation
    recommendation_info_without_ai = SimpleOrderRecommendation.objects.filter(
        computer_id = id, recommendation_id = time).first()
    
    if recommendation_info_ai is not None:
        # Recuperer tous les details de l'ordinateur
        recommend = recommended_object_builder(relevant_computer, computer_images, recommendation_info_ai)
        

    elif recommendation_info_without_ai is not None:
        # Recuperer tous les details de l'ordinateur
        recommend = recommended_object_builder(relevant_computer, computer_images, {"choose_reason":None})
        
    else:
        recommend = recommended_object_builder(relevant_computer, computer_images, {"choose_reason":None})
        
        # return render(request, "api_444_error.html")
    request.session["time"] = time # mis dans la session pour le code qr
    context = {
        "page_title":"detail.ph",
        "computer_details":recommend,
        "id_computer":id,
        "time_info":time,
        "accessoirs":ComputerAcessoirsInfo.objects.filter(computer=relevant_computer.id, is_applied=True)
    }
    return render(request,"detail.html", context)


from decimal import Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # You can also use str(obj) for higher precision
        return super(DecimalEncoder, self).default(obj)
    
def select_computers(budgetMin, max_price_set):
    """
    Sélectionne 50 ordinateurs dont le prix est compris dans l'intervalle [budgetMin, max_price_set]
    en deux étapes:
    1. Sélectionne les ordinateurs des partenaires (max 30);
    2. Sélectionne les ordinateurs non-partenaires pour compléter jusqu'à 50 (si nécessaire);
    3. Combine les deux QuerySets (partenaires et non-partenaires) pour obtenir la sélection finale.
    
    :param budgetMin: le prix minimum de l'ordinateur
    :type budgetMin: int
    :param max_price_set: le prix maximum de l'ordinateur
    :type max_price_set: int
    :return: une QuerySet de Computer, contenant 50 ordinateurs satisfaissant les critères
    :rtype: QuerySet<Computer>
    """
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


# Commander avec l'ia
@require_http_methods(["GET", "POST"])
def withai_recommendation(request):
    """
    Traitement de la requête de recommendation d'un ordinateur.
    
    Si la requête est de type POST, alors on récupère les informations du formulaire,
    on calcule le prix maximal que l'utilisateur est prêt à payer, on selectionne les
    ordinateurs en fonction de ce prix et de la marge de tolérance, on enregistre les
    informations sur l'utilisateur qui a fait la requête, on crée un fichier contenant
    la liste des ordinateurs à recommander, on utilise l'IA pour faire la recommandation
    et on enregistre le résultat de la recommandation.
    
    Si la requête est de type GET, alors on renvoie la page de formulaire de
    recommandation.
    
    :param request: La requête HTTP.
    :return: La page HTML correspondante.
    """
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
                            "image": cover_image.image.url if cover_image else cover_image.url,
                            "price": float(computer_instance.price_amount),
                            "color":computer_instance.color.color,
                            "processor": f'{computer_instance.processor.model}',
                            "brand":computer_instance.brand.name,
                            "ram": computer_instance.memory.capacity,
                            "storage": computer_instance.storages.first().capacity,
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

# Enregistrer la comande
from datetime import datetime, timedelta
@require_POST
def processOrderPage(request):
    """
    Handles the order processing request for a computer purchase.

    This function expects a POST request with a JSON payload containing customer 
    and order details. It validates the request data, checks for the existence 
    of the specified computer, and verifies if a similar order already exists. 
    If the order doesn't already exist, it creates a new order with an estimated 
    delivery date and saves it to the database.

    JSON payload should include:
    - first_name: Customer's first name.
    - last_name: Customer's last name.
    - phone: Customer's phone number.
    - location: Delivery location.
    - id_computer: ID of the computer being ordered.
    - number_of_item: Quantity of the computer being ordered.

    Returns:
    - JsonResponse with status 200 and a success message if the order is created successfully.
    - JsonResponse with status 404 if the specified computer is not found.
    - JsonResponse with status 200 if the order already exists.
    - JsonResponse with status 400 if the request contains invalid JSON.
    - JsonResponse with status 500 if any other exception occurs.
    """
    try:
        data = json.loads(request.body)
        first_name = data.get('first_name', '')
        last_name  = data.get('last_name', '') 
        phone      = data.get('phone', '00 00 00 00')
        location   = data.get('location', '')
        computer   = data.get('id_computer', '')
        number     = data.get('number', '')

        # print(request.body)
        # Check if the computer exists
        relevant_computer = Computer.objects.filter(pk=computer).first()
        if not relevant_computer:
            return JsonResponse({"message": "Computer not found"}, status=404)
        
        # Check if the order already exists
        instance_commend = Commend.objects.filter(
            first_name=first_name,
            last_name=last_name,
            computer=relevant_computer,
            phone=phone, location=location,
            number=number           
        )
        if instance_commend.exists():
            # Update the existing order to be traited again
            instance_commend.first().is_traited = False
            pos = instance_commend.first()
            pos.save()

            request.session["computer_recommended"] = pos.pk
            return JsonResponse({"message": "Order updated successfully"}, status=200)
        
        # Save the new order
        delivery_date = datetime.now().date() + timedelta(days=3)
        isinstance_order = Commend(
            first_name=first_name,
            last_name=last_name,
            computer=relevant_computer,
            phone=phone,
            location=location,
            delivery_date=delivery_date,
            number=number
        )
        isinstance_order.save()
        request.session["computer_recommended"] = isinstance_order.pk

        return JsonResponse({"message": "Order created successfully"}, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON format"}, status=400)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)


# Commander sans l'ia
@require_POST
def performSimpleOrder(request):

    """
    Permet de traiter une requête de recommendation d'un ordinateur.
    
    L'utilisateur envoie les informations de l'ordinateur qu'il recherche 
    (marque, ram, processeur, stockage) ainsi que les caracteristiques 
    supplémentaires qu'il souhaite (carte graphique, processeur, etc.).
    
    La fonction renvoie une liste d'ordinateurs pertinents en fonction des 
    informations envoyées par l'utilisateur.
    
    :param request: La requête HTTP.
    :return: Un JSON contenant la liste des ordinateurs pertinents.
    """
    data     = json.loads(request.body)
    computer = data.get("computer", "")
    characteristics = data.get('characteristics', "")
    id_result = None # Id du resultat de la recommandation. (datetime de l'enregistrement de la requête)

    # Recherche de l'ordinateur
    if len(computer) != 0 :
        brand = computer.get('brand', '')
        ram   = computer.get('ram', 0)
        processor_core = computer.get('processor', '').get('core', 0)
        processor_core = int(processor_core) + 1 # CORE - 1 is send to user
        storage    = computer.get('storage', '')
        budget_min = computer.get('budget', '').get('min', '')
        budget_calculated_max = computer.get('budget', '').get('calculatedMax', '0 FCFA')
        # budget_max = computer.get('budget', '').get('max', '')
        # budget_tolerance      = computer.get('budget', '').get('tolerance', '')
        budget_calculated_max = budget_calculated_max.split(" ")[0] 
        storage = storage.split(" ")[0] + " "+ storage.split(" ")[1]

        # Recherche des ordinateurs pertinents repondant aux besoins de l'utilisateur
        relevant_computers = Computer.objects.filter(
            processor__cores=processor_core, memory__capacity=ram,
            storages__capacity=storage, brand__name=brand,
            price_amount__range=(int(budget_min), int(budget_calculated_max))
        )
        
        # Prise en compte des caractéristiques supplémentaires
        result_relevant_computers = []
        if relevant_computers.exists():
            if len(characteristics) != 0:
                result_relevant_computers     = charateristiqueRelevantComputer(relevant_computers,characteristics)
            else:
                result_relevant_computers    = relevant_computers

        # Un ordinateur avec une carte graphique à ce prix est pertinent
        graphicalComputerOnThePrice = graphicForGoodComputer(
            Computer, int(budget_min), int(budget_calculated_max))
        
        # Un ordinateur avec une ram >= 8 à ce prix est pertinent
        ramComputerOnThePrice = ramForGoodComputer(
            Computer, int(budget_min), int(budget_calculated_max),8)
        
        # Un ordinateur avec un processeur >= 4 à ce prix est pertinent
        processorComputerOnThePrice = processorForGoodComputer(
            Computer, int(budget_min), int(budget_calculated_max), 4)
        
        # Un ordinateur avec un stockage >= 512 à ce prix est pertinent
        storageComputerOnThePrice = storageForGoodComputer(
            Computer, int(budget_min), int(budget_calculated_max), 512, 'SSD')
        
        # Fusion des ordinateurs pertinents pour constituer le resultat de la recommendation
        result_final = mergeSimpleOrderComputer(result_relevant_computers,
            graphicalComputerOnThePrice, ramComputerOnThePrice,
            processorComputerOnThePrice, storageComputerOnThePrice)
        
        # print(result_final) 
        # Enregistrement des recommendations dans la base de données: Persistance
        user_id = get_client_ip(request) # Ip de l'utilisateur
        user_location = get_location_by_ip(user_id) # location de l'utilisateur via l'ip

        id_result = recommendationPersistance(SimpleOrderRecommendation,result_final, 
            user_id, user_location, int(budget_min), int(budget_calculated_max),
            characteristics.get('carte_graphique', ''), brand, ram, storage, processor_core,
            characteristics.get('Vitesse_processeur', ''), characteristics.get('Systeme_exploitation', ''),
            characteristics.get('couleur', ''))
    else:
        return JsonResponse({"message": "error"}, status=500)
    
    return JsonResponse({"message": "success", "id_result": id_result}, status=200)


def displaySimpleOrderRecommendation(request, id):
    """
    This view displays the recommendation of computers based on the id (time) of the recommendation passed in the url.

    The view will retrieve the recommendation from the database and render the recommendation.html template with the following data:

    - recommendation: a list of dictionaries containing the id, model, time, image, price, color, processor, brand, ram and storage of the recommended computers
    - minBudget: the minimum budget of the recommendation
    - maxBudget: the maximum budget of the recommendation
    - computerBrands: all the brands of computers
    - computerColors: all the colors of computers
    - computerRAMS: all the ram of computers

    If the id is not provided or the recommendation does not exists in the database, the view will return a 404 error.

    :param request: The request object
    :param id: The id of the recommendation
    :return: The rendered html page
    """

    computer_recommended = []
    if id is None:
        return render(request, 'api_444_error.html', {})
    computer_instances = SimpleOrderRecommendation.objects.filter(recommendation_id=id)

    if not computer_instances.exists():
        return render(request, 'api_444_error.html', {})
    
    for r in computer_instances:
        computer_instance = Computer.objects.filter(pk=r.computer_id).first()
        cover_image       = ComputerPhoto.objects.filter(computer=computer_instance, is_cover=True).first()
        computer_recommended.append({
            "id": r.computer_id,
            "model":computer_instance.model,
            "time": id,
            "image": cover_image.image.url if cover_image else cover_image.url,
            "price": float(computer_instance.price_amount),
            "color":computer_instance.color.color,
            "processor": f'{computer_instance.processor.model}',
            "brand":computer_instance.brand.name,
            "ram": computer_instance.memory.capacity,
            "storage": computer_instance.storages.first().capacity,
        })
    

    budgetMin     = computer_instances.first().min_budget
    max_price_set = computer_instances.first().max_budget

    return  render(request,"recommendation.html", {
                        "recommendation":json.dumps(computer_recommended, cls=DecimalEncoder),
                        "minBudget":budgetMin,
                        "maxBudget":max_price_set,
                        "computerBrands":Brand.objects.all(),
                        "computerColors":ComputerColor.objects.all(),
                        "computerRAMS":Memory.objects.all()
                        })


# Pdf 
from .render_html_to_pdf import render_html_to_pdf

def downloadOrderPdf(request):
    
    """
    Permet de télécharger la commande en format PDF.
    
    La fonction prend comme paramètre la requête.
    Elle récupère l'instance de la commande associée à la session.
    Elle crée un dictionnaire contenant les informations de la commande.
    Elle appelle la fonction render_html_to_pdf pour convertir le modèle HTML en PDF.
    """
    
    id_command = request.session["computer_recommended"]

    commande_instance  = Commend.objects.filter(
        id = id_command
    ).first()
    
    time = request.session["time"] if "time" in request.session else ""

    data = {
        "computer_id":commande_instance.computer.id,
        "user_name":f"{commande_instance.first_name } {commande_instance.last_name }",
        "computer_brand":commande_instance.computer.brand,
        "computer_processeur":commande_instance.computer.processor.model,
        "computer_ram":commande_instance.computer.memory.capacity,
        "computer_storage":commande_instance.computer.storages.first().capacity,
        "computer_color":commande_instance.computer.color.color,
        "user_phone":commande_instance.phone,
        "time":time,
        "computer_quantite":commande_instance.number
    }

    return render_html_to_pdf('pdf/pdf.html', data)



# 404 pas d'url
from django.http import Http404
from django.shortcuts import render

def error_404(request, exception):
    print("ok")
    return redirect("error_404")