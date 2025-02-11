from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Custom user manager that handles the creation of User instances.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Ensure an email address is provided; if not, raise a ValueError.
        if not email:
            raise ValueError('An email address is required')
        
        # Normalize the email address by lowercasing the domain part.
        email = self.normalize_email(email)
        
        # Create a new user instance with the given email and any additional fields.
        user = self.model(email=email, **extra_fields)
        
        user.set_password(password)
        
        # Save the user instance to the database.
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        # Set default values for a superuser.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Validate that the provided fields meet superuser requirements.
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # Create a superuser using the create_user method.
        return self.create_user(email, password, **extra_fields)

# Custom User model that replaces the default Django User.
# Inherits from AbstractBaseUser for core authentication and PermissionsMixin for permission support.
class User(AbstractBaseUser, PermissionsMixin):
    # Unique email field used as the identifier for authentication.
    email = models.EmailField(unique=True)
    
    # Optional fields for storing the user's details
    first_name = models.CharField(max_length=30, blank=True)
    last_name  = models.CharField(max_length=30, blank=True)
    
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # Field indicating if the user can access the admin site.
    is_staff = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)

    # Set the custom manager for handling user creation.
    objects = CustomUserManager()

    # Define the field to be used as the unique identifier for authentication.
    USERNAME_FIELD = 'email'
    
    # List of additional required fields when creating a user via the command line.
    # Email and password are required by default.
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# Company model represents a company entity in the system.
class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
