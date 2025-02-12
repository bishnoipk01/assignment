from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Company, User
from .forms import UserForm
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.views import LoginView

from .forms import UserRegistrationForm

class CustomLoginView(LoginView):
    """ Prevents logged-in users from accessing the login page """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/') 
        return super().dispatch(request, *args, **kwargs)


# new user registration
def register(request):
    if request.user.is_authenticated:
        return redirect('/')  # Redirect to the home page if the user is already logged in.
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the new user.
            # log the user in immediately after registration:
            user = authenticate(email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'))
            if user is not None:
                login(request, user)
                # Redirect to the home page after successful registration and login.
                return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


# Company detail view (requires login)
@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, 'company_detail.html', {'company': company})

# User detail view (requires login) – only allow users to see their own details
@login_required
def user_detail(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.user != user:
        return HttpResponse("Unauthorized", status=401)
    return render(request, 'user_detail.html', {'user_obj': user})

# User edit view (requires login)
@login_required
def user_edit(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.user != user:
        return HttpResponse("Unauthorized", status=401)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=user.pk)
    else:
        form = UserForm(instance=user)
    return render(request, 'user_edit.html', {'form': form})


def home(request):
    if not request.user.is_authenticated:
        # User is not logged in; send them to the login page.
        return redirect('login')
    
    companies = Company.objects.all()
    return render(request, 'home.html', {'companies': companies})



    
    
