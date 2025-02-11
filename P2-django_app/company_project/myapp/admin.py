from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Company

# Custom admin class for our custom User model.
# This class extends Django's built-in UserAdmin to provide a tailored
# admin interface for managing users.
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    
    search_fields = ('email', 'first_name', 'last_name')
    
    # Set the default ordering of users in the list view.
    ordering = ('email',)
    
    # Define how the fields are grouped on the user detail (edit) page.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    # Define the layout for the "add user" form in the admin.
    # This configuration is used when creating a new user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  
            'fields': ('email', 'password1', 'password2'),  
        }),
    )

# Register the custom User model with the admin site 
admin.site.register(User, UserAdmin)

# Register the Company model with the admin site.
admin.site.register(Company)
