from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # login if register successful
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']  # Corrected the password access
            user = authenticate(request, email=email, password=password)
            login(request, user)

            messages.success(request, 'Registered successfully')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register_user.html', {'form': form})

def login_user(request):
	if request.method == "POST":
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			# Return an 'invalid login' error message.
			messages.success(request, ("error for login in"))
			return redirect('login_user')
	else:
		return render(request, 'users/login_user.html', {})
	
@login_required
def logout_user(request):
	logout(request)
	messages.success(request, ("You were logged out"))
	return redirect('home')

@login_required
def account(request):
	return render(request, 'users/account.html', {})