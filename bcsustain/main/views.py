from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def rewards(request):
    return render(request, 'rewards.html')

def supervisorrewards(request):
    return render(request, 'supervisorrewards.html')

def add_reward(request):
    if request.method == 'POST':
        # Logic for adding the reward (e.g., save to database)
        # For now, you can simply redirect back to the supervisor rewards page after processing.
        return redirect('supervisorrewards')
    else:
        return HttpResponse("Invalid request method", status=400)
def action(request):
    return render(request, 'action.html')
def base(request):
    return render(request, 'base.html')

def supervisor(request):
    return render(request, 'supervisorLandingPage.html')
