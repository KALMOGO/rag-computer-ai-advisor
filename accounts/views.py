# accounts/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json

@csrf_protect
@require_http_methods(["POST"])
def login_view(request):
    # Verifier le temps d'essai
    if "tryTime" not in request.session:
        request.session["tryTime"] = 0
    request.session["tryTime"] += 1

    tryTime = request.session["tryTime"]
    error_message = "Vous n'etes pas autorisé à vous connecter !"

    try:
        data = json.loads(request.body) if request.body else request.POST
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        keyword = data.get('keyword', '').strip()
        
        if not all([email, password]):
            return JsonResponse({
                'success': False,
                'message': error_message,
                'tryTime': tryTime
            }, status=400)
            
        user = authenticate(
            request,
            username=email,  # authentication backend uses username parameter
            password=password,
            keyword=keyword
        )
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': "Login successful",
                    'user': {
                        'email': user.email,
                        'keyword': user.keyword,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                }, status=200)
            else:
                print("ok")
                # Session reset
                if request.session["tryTime"] >= 3:
                    request.session["tryTime"] = 0
                
                return JsonResponse({
                    'success': False,
                    'message': error_message,
                    'tryTime': tryTime
                }, status=403)
        else:
            # Session reset
            if request.session["tryTime"] >= 3:
                request.session["tryTime"] = 0

            return JsonResponse({
                'success': False,
                'message': error_message,
                'tryTime': tryTime
            }, status=401)
            
    except json.JSONDecodeError:
        # Session reset
        if request.session["tryTime"] >= 3:
            request.session["tryTime"] = 0

        return JsonResponse({
            'success': False,
            'message': error_message,
            'tryTime': tryTime
        }, status=400)
    
    except Exception as e:
        # Session reset
        if request.session["tryTime"] >= 3:
            request.session["tryTime"] = 0

        return JsonResponse({
            'success': False,
            'message': error_message,
            'tryTime': tryTime
        }, status=500)

@login_required
def logout_view(request):
    logout(request)
    return JsonResponse({
        'success': True,
        'message': "Logout successful"
    }, status=200)