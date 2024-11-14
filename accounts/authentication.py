# accounts/authentication.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Handle both email and keyword authentication
            email = username if username else kwargs.get('email')
            keyword = kwargs.get('keyword')
            
            if email is None:
                return None
            
            # Basic query with email
            query = Q(email__iexact=email)
            
            # Add keyword to query if provided
            if keyword:
                query &= Q(keyword=keyword)
            
            user = UserModel.objects.get(query)
            
            # Check the password and is_active flag
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
                
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce timing
            # attacks targeting a particular user
            UserModel().set_password(password)
            return None
        except Exception:
            return None
            
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None