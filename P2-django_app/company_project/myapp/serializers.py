from rest_framework import serializers
from .models import Company, User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class CustomAuthTokenSerializer(serializers.Serializer):
    # Define input field for the user's email and password
    email = serializers.EmailField(label="Email")

    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user based on email and password.
        """
        # Extract the email and password from the incoming data.
        email = attrs.get('email')
        password = attrs.get('password')

        # Ensure both email and password are provided.
        if email and password:
            # Since the custom user model sets USERNAME_FIELD = 'email',
            # we pass the email to authenticate() as the 'username' argument.
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            # If authentication fails, raise a validation error.
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            # Raise an error if either field is missing.
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        # On success, attach the authenticated user object to the validated data.
        attrs['user'] = user
        return attrs


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # Make password a required, write-only field with a minimum length.
    password = serializers.CharField(
        write_only=True, required=True, min_length=8
    )

    class Meta:
        model = User
        # Include the password field here so that it is validated on creation.
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'phone_number', 'bio']
    
    def create(self, validated_data):
        # Remove the password from validated_data before passing it to the create_user method
        password = validated_data.pop('password')
        # Use create_user to handle proper password hashing
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

