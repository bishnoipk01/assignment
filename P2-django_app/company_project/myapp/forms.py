from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User

# Custom login form
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

# Form to allow users to update their own details
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        # Exclude the email field since it should not be changed,
        # and include new fields like phone_number and bio.
        fields = ['first_name', 'last_name', 'phone_number', 'bio']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        # The UserCreationForm automatically includes password1 and password2 fields.
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
