from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from .forms import SupervisorForm
from .models import Campaign
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

@login_required
def profile_setup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('landing')  # Redirect to landing page after saving profile
    else:
        form = ProfileForm()
    return render(request, 'profile_setup.html', {'form': form})


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
    today = timezone.now().date()  # Get the current date
    active_campaigns = Campaign.objects.filter(start_date__lte=today, end_date__gte=today)  # or any condition for "active"
    past_campaigns = Campaign.objects.filter(end_date__lt=today)
    # Pass the list of active campaigns to the template
    context = {
        'active_campaigns': active_campaigns,
        'past_campaigns': past_campaigns,
    }
    return render(request, 'supervisorLandingPage.html', context)

def landing(request):
    return render(request, 'landing.html')
def campaign_form(request):
    return render(request, 'campaign_form.html')

# Check if the user is a superuser
def is_superuser(user):
    return user.is_superuser

@user_passes_test(lambda u: u.is_superuser)
def manage_supervisors(request):
    User = get_user_model()
    users = User.objects.all()

    if request.method == 'POST':
        form = SupervisorForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            user.is_supervisor = form.cleaned_data['is_supervisor']
            user.save()
            return redirect('manage_supervisors')

    return render(request, 'manage_supervisors.html', {'users': users})

# def manage_supervisors(request):
#     return render(request, 'manage_supervisors.html')

# @user_passes_test(is_superuser)
# def manage_supervisors(request):
#     User = get_user_model()
#     users = User.objects.all()

#     if request.method == 'POST':
#         form = SupervisorForm(request.POST)
#         if form.is_valid():
#             user_id = request.POST.get('user_id')
#             user = User.objects.get(id=user_id)
#             user.is_supervisor = form.cleaned_data['is_supervisor']
#             user.save()
#             return redirect('manage_supervisors')

#     return render(request, 'manage_supervisors.html', {'users': users})


def profile_setup(request):
    return render(request, 'profile_setup.html')


def campaign_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        points = request.POST.get('points')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        location = request.POST.get('location')
        description = request.POST.get('description')
        delivery_method = request.POST.get('delivery_method')
        add_to_news = request.POST.get('add_to_news') == 'on'

        # Save the campaign to the database
        Campaign.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            location=location,
            description=description,
            is_active=True  # Mark campaign as active upon creation
        )

        return redirect('supervisor')  # Redirect to the supervisor page
    return render(request, 'campaign_form.html')