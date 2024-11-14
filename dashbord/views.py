from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
import json

from article.computers.models import *
from article.orders.models import *
from main.models import *

from .dashbord_tools_utils import *

# Create your views here.

def authentication(request):
    # ckeck if the tryTime exist in the session
    if "tryTime" not in request.session:
        request.session["tryTime"] = 0
    context = {
        "page_title":"connection.ph",
    }
    return render(request,"dashbord-templates/dashbord-connexion.html", context)

def logoutUser(request):
    """
    Log out the user if the user is authenticated and redirect to the authentication page

    Args:
        request (HttpRequest): the request object

    Returns:
        HttpResponse: the response to the request
    """

    if request.user.is_authenticated:
        logout(request)
    return redirect("/dashbord")


def index(request) :
    # check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect("/dashbord")
    
    context = {
        "page_title":"index.ph",
    }
    return render(request,"dashbord-templates/dashbord-index.html", context)

def profile(request) :
    # check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect("/dashbord")
    
    context = {
        "page_title":"profile.ph",
    }
    return render(request,"dashbord-templates/dashbord-userprofile.html", context)

def register(request) :
    # check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect("/dashbord")
    context = {
        "page_title":"register.ph",
    }
    return render(request,"dashbord-templates/dashbord-createaccount.html", context)

def supplier(request) :
    # check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect("/dashbord")
    context = {
        "page_title":"supplier.ph",
    }
    return render(request,"dashbord-templates/dashbord-addsupplier.html", context)

def computer_list(request) :
    # check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect("/dashbord")
    context = {
        "page_title":"computer-list.ph",
    }
    return render(request,"dashbord-templates/dashbord-addcomputer.html", context)

def add_computer_photo(request) :
    # check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect("/dashbord")
    context = {
        "page_title":"add-computer-photo.ph",
    }
    return render(request,"dashbord-templates/dashbord-addcomputerphoto.html", context)

def add_computer(request) : 
    """
    Returns a rendered HTML page with a form to add a new computer.

    The page displays a form with the following fields:
        - a dropdown to select the brand
        - a dropdown to select the color
        - a dropdown to select the processor
        - a dropdown to select the memory
        - a dropdown to select the graphics
        - a dropdown to select the motherboard
        - a dropdown to select the power supply
        - a dropdown to select the cooling
        - a dropdown to select the operating system
        - a dropdown to select the keyboard
        - a dropdown to select the supplier
        - a dropdown to select the storage
        - a checkbox list to select the pre-installed software

    The form will be processed by the perform_add_computer view.

    :param request: The HTTP request object.
    :return: A rendered HTML page.
    """
    # check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect("/dashbord")
    context = {
        "page_title":"add-computer.ph",
        "brands":Brand.objects.all(),
        "colors":ComputerColor.objects.all(),
        "processors":Processor.objects.all(),
        "memories":Memory.objects.all(),
        "graphics":Graphics.objects.all(),
        "motherboards":Motherboard.objects.all(),
        "powersupplies":PowerSupply.objects.all(),
        "coolings":Cooling.objects.all(),
        "operating_systems":OperatingSystem.objects.all(),
        "keyboards":ComputerKeyboard.objects.all(),
        "suppliers":Supplier.objects.all(),
        "storages":Storage.objects.all(),
        "preInstalledSofwares":ListSofware.objects.all()
    }
    return render(request,"dashbord-templates/dashbord-addcomputer.html", context)


@require_POST
@login_required
def perform_add_computer(request):
    """
    Handles the addition of a new computer to the database.

    This view function processes a POST request containing JSON data that 
    describes the attributes and specifications of a computer. It validates 
    and parses the data, handles foreign key relationships, and creates a 
    new Computer object in the database. If successful, it returns a JSON 
    response with the computer's details. In case of errors, it returns an 
    appropriate JSON response with error details.

    :param request: The HTTP request object containing JSON data.
    :return: JsonResponse with success or error details.
    """
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)

        # print(data)
        # Process numeric fields with validation
        numeric_fields = {
            'display_ports': int(data.get('display_ports', 0)),
            'hdmi_ports': int(data.get('hdmi_ports', 0)),
            'usb2_0': int(data.get('usb2_0', 0)),
            'usb3_2_gen1_typeA': int(data.get('usb3_2_gen1_typeA', 0)),
            'usb3_2_gen2_typeA': int(data.get('usb3_2_gen2_typeA', 0)),
            'usb3_2_gen2_typeC': int(data.get('usb3_2_gen2_typeC', 0)),
            'price_amount': float(data.get('price_amount', 0)),
            'percentage': float(data.get('percentage', 0)),
        }

        # Process foreign key relationships
        motherboard_id = data.get('motherboard') # La valeur par defaut cause des erreurs souvant
        power_supply_id = data.get('power_supply')
        graphics_id = data.get('graphics')
        keyboard_id = data.get('keyboard')
        color_id    = data.get('color')
        cooling_id  = data.get('cooling')
        if motherboard_id:
            motherboard = Motherboard.objects.get(id=int(motherboard_id))
        else:
            # Handle the case where 'motherboard' is not present or is an empty string
            motherboard = None
        if power_supply_id:
            power_supply = PowerSupply.objects.get(id=int(power_supply_id))
        else:
            power_supply = None
        if graphics_id:
            graphics =  Graphics.objects.get(id=int(graphics_id))
        else:
            graphics = None
        if keyboard_id:
            keyboard =  ComputerKeyboard.objects.get(id=int(keyboard_id))
        else:
            keyboard = None
        if color_id:
            color = ComputerColor.objects.get(id=int(color_id))
        else:
            color=None
        if cooling_id:
            cooling =  Cooling.objects.get(id=int(cooling_id))
        else:
            cooling = None

        foreign_keys = {
            'brand': Brand.objects.get(id=int(data.get('brand', 0))),
            'color': color,
            'cooling': cooling,
            'memory': Memory.objects.get(id=int(data.get('memory',0))),
            'motherboard': motherboard,
            'operating_system': OperatingSystem.objects.get(id=int(data.get('operating_system',0))),
            'power_supply':power_supply,
            'processor': Processor.objects.get(id=int(data.get('processor',0))),
            'supplier': Supplier.objects.get(id=int(data.get('supplier',0))),
            'graphics': graphics,
            'keyboard': keyboard,   
        }
        # Create computer object
        computer = Computer(
            # Basic information
            model=data.get('model'),
            type=data.get('type'),
            description=data.get('description', ''),

            # Foreign key fields
            **foreign_keys,
            
            # Numeric fields
            **numeric_fields,
            
            # Connectivity
            bluetooth=data.get('bluetooth', ''),
            ethernet=data.get('ethernet', ''),
            wifi=data.get('wifi', ''),
            
            # Audio
            audio_front_panel=data.get('audio_front_panel', ''),
            audio_rear_panel=data.get('audio_rear_panel', ''),
            
            # Physical specifications
            height=data.get('height', ''),
            width=data.get('width', ''),
            depth=data.get('depth', ''),
            weight=data.get('weight', ''),
            
            # Additional features
            
            extras=data.get('extras', ''),
            
            # Warranty information
            warranty_duration=data.get('warranty_duration', ''),
            warranty_type=data.get('warranty_type', ''),
            warranty_support=data.get('warranty_support', ''),
            
            # Shipping
            estimated_shipping_time=data.get('estimated_shipping_time', ''),
            
            # Price and currency
            price_currency=data.get('price_currency', 'CFA'),
            
            # Rating information
            average_rating=float(data.get('average_rating', 0.01)),
            number_of_reviews=int(data.get('number_of_reviews', 0.01)),
        )
        # Save the computer now
        computer.save()

        # Save storage info in Staroges
        storage_id= data.get('storage')
        storages = Storage.objects.filter(id=int(storage_id))
        for storage in storages:
            computer.storages.add(storage)


        return JsonResponse({
            'status': 'success',
            'message': 'Computer added successfully',
            'data': {
                'id': computer.pk,
                'model': computer.model,
                'type': computer.type,
                'price': str(computer.price_amount),
                'currency': computer.price_currency,
            }
        })
    except (ValueError, ValidationError) as e:
        print(e)
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'error_type': 'validation_error'
        }, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({
            'status': 'error',
            'message': 'An unexpected error occurred',
            'error_type': 'server_error',
            'detail': str(e)
        }, status=500)

@csrf_exempt
@login_required
def perform_add_computer_images(request) :
    """
    Handle adding images to a computer
    This view is called from the add computer form and expects a POST request with the following data:
    """
    if request.method == 'POST':
        computer_id = request.POST.get('computer_id', '0')

        # You might need to create this instance or get it from the database
        computer = Computer.objects.get(id=computer_id)  # Replace 'some_id' with actual computer ID

        # Handle cover image
        cover_image = request.FILES.get('cover-image')
        if cover_image:
            try:
                ComputerPhoto.objects.create(
                    computer=computer,
                    image=cover_image,
                    is_cover=True,
                    slug="cover-image",  # You might want to generate this dynamically
                    url=""  # Set this if needed
                )
            except Exception as e:
                print(e)
                JsonResponse({'error': 'Invalid request method'}, status=405)

        # Handle additional images
        for i in range(1, 5):
            image = request.FILES.get(f'image-{i}')
            if image:
                try:
                    ComputerPhoto.objects.create(
                        computer=computer,
                        image=image,
                        is_cover=False,
                        slug=f"image-{i}",  # You might want to generate this dynamically
                        url=""  # Set this if needed
                    )
                except Exception as e:
                    print(e)
                    return JsonResponse({'error': 'Invalid request method'}, status=500)
        return JsonResponse({'message': 'Images uploaded successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
  
@csrf_exempt
@login_required
def savePreInstalledSoftwares(request):
    """ Enregistrement des ordinateurs preInstallés """
    # Convertir en dict le json venant
    data = json.loads(request.body)
    # Recuperation des données envoyés
    computer_id = data.get("computer_id",0)
    selectedSoftware = data.get("selectedSoftware","")
    # print("ok",selectedSoftware)
    # print("",computer_id)

    # Recuperation de l'ordinateur
    computer    = Computer.objects.filter(
        id = computer_id
    ).first()
    if computer is not None: #Si l'ordi exist
        try:
            # Enregistrer tous les logiciels pre installé
            for software_id in selectedSoftware: 
                # Recuperation du logiciels dans la table intermedière contenant l'ordi
                software_list = ListSofware.objects.filter(id=int(software_id))
                for software in software_list: # une seul fois run
                    # Enregistrement de l'ordi
                    preInstalledSoftware_instance = PreInstalledSoftware(
                        name=software.name,
                        version=software.version,
                        description=software.description,
                        computer=computer
                    )
                    preInstalledSoftware_instance.save()
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Invalid request method'}, status=500) 
        return JsonResponse({'message': 'uploaded successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
  
def processed_orders(request) :
    # check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect("/dashbord")
    
    orders = [get_orders_data(order) for order in Commend.objects.filter(is_traited=True)],
    context = {
        "page_title":"processed-orders.ph",
        "orders":json.dumps(orders)
    }
    return render(request,"dashbord-templates/dashbord-processedorders.html", context)

def unproccessedorders(request) :
    # check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect("/dashbord")
    
    orders = [get_orders_data(order) for order in Commend.objects.filter(is_traited=False)],
    context = {
        "page_title":"unproccessedorders.ph",
        "orders":json.dumps(orders)
    }
    return render(request,"dashbord-templates/dashbord-unproccessedorders.html", context)



@csrf_exempt  # Use this only if you are handling CSRF tokens manually
@require_http_methods(["PATCH"])  
def update_order_status(request, order_id):
    # Get the order from the database
    order = get_object_or_404(Commend, pk=order_id)

    # Check if order is empty
    if not order:
        return JsonResponse({"error": "Commande introuvable !"}, status=404)
    
    # Update the order status
    order.is_traited = True  # Update based on incoming data
    order.save()
    return JsonResponse({"message": "Commande traitée avec succès !"}, status=200)


@csrf_exempt 
@require_http_methods(["DELETE"])  
def detete_order(request, order_id):
    order = get_object_or_404(Commend, pk=order_id)
    if not order:
        return JsonResponse({"error": "Commande introuvable !"}, status=404)
    order.delete()
    return JsonResponse({"message": "Commande supprimée avec succès !"}, status=200)
