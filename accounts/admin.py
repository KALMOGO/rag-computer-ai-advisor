# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'keyword', 'username', 'tel1', 'tel2', 'photo', 
                 'is_active', 'is_staff', 'is_superuser')

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'keyword', 'username', 'tel1', 'tel2', 'photo')

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    # Customize list display
    list_display = ('email', 'keyword', 'username', 'tel1', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    
    # Fields for editing an existing user
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('keyword', 'username', 'tel1', 'tel2', 'photo', 'last_name', 'first_name')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'keyword', 'username', 'tel1', 'tel2', 'photo',
                      'password1', 'password2'),
        }),
    )
    
    search_fields = ('email', 'keyword', 'username', 'tel1', 'tel2')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_readonly_fields(self, request, obj=None):
        # Make certain fields readonly in edit mode
        if obj:  # editing an existing object
            return ('date_joined', 'last_login')
        return ()

# Register the model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)