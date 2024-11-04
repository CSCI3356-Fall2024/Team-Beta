from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from .forms import SupervisorForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import logout as auth_logout
from .forms import CampaignForm
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from .models import Campaign
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib import messages

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

def logout(request):
    auth_logout(request)
    return redirect('login')  # Redirect to the login page after logout


# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Check if email ends with @bc.edu
        if not email.endswith('@bc.edu'):
            messages.error(request, "Please use a valid @bc.edu email address.")
            return render(request, 'signup.html', {'form': form})

        # Check if passwords match
        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html', {'form': form})

        # Check if email already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'signup.html', {'form': form})

        # If the form is valid, create and log in the user
        if form.is_valid():
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            auth_login(request, user)
            return redirect('landing')  # Redirect to a landing page or dashboard
        else:
            # If form is not valid, render form with errors
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()  # Initialize a blank form if it's a GET request

    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
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

    ongoing_tasks = [
    {
        'name': 'Green2Go Box',
        'points': 12,
        'time': 'Ongoing',
        'image': 'green2go.png'
    }
    ]
    events = [
        {
            'name': 'Sustainability Talk',
            'points': 10,
            'date': '01/01/2024',
            'image': 'noimage.png'
        },
        {
            'name': 'Climate Change Webinar',
            'points': 20,
            'date': '02/01/2024',
            'image': 'noimage.png'
        }
        ]

    volunteer_work = [
        {
            'name': 'Community Clean-Up',
            'points': 15,
            'date': '03/01/2024',
            'image': 'noimage.png'
        },
        # Add more volunteer work as needed
    ]

    context = {
        'ongoing_tasks': ongoing_tasks,
        'events': events,
        'volunteer_work': volunteer_work,
    }
    return render(request, 'action.html', context)


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

#@login_required
def landing(request):
    # Check if the user is authenticated and their profile is complete
    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        if profile and not profile.is_complete():
            # Redirect to profile setup if incomplete
            return redirect('profile_setup')

        # Determine the user's role (Supervisor or Student) if logged in
        role = "Supervisor" if profile and profile.is_supervisor else "Student"
    else:
        role = "Not Logged in. For Testing"  # Not logged in

    # Get active campaigns for today
    today = timezone.now().date()
    active_campaigns = Campaign.objects.filter(
        start_date__lte=today,
        end_date__gte=today,
        add_to_news=True
    )

    # Pass the active campaigns and role to the template
    return render(request, 'landing.html', {
        'active_campaigns': active_campaigns,
        'role': role,
    })

def campaign_form(request):
    return render(request, 'campaign_form.html')

# Check if the user is a superuser
def is_superuser(user):
    return user.is_superuser

@user_passes_test(lambda u: u.is_superuser)
# def manage_supervisors(request):
#     # Ensure all users have a profile
#     for user in User.objects.all():
#         Profile.objects.get_or_create(user=user)

#     # Retrieve all users with profiles to display in the template
#     users = User.objects.all()

#     if request.method == 'POST':
#         print("POST request received")  # Debugging
#         form = SupervisorForm(request.POST)
#         form.save()
#         if form.is_valid():
#             print("Form is valid")  # Debugging
#             user_id = request.POST.get('user_id')
#             print(f"User ID received: {user_id}")  # Debugging

#             # Check that `user_id` is correctly retrieved
#             if not user_id:
#                 print("No user_id found in POST data.")
#                 return redirect('manage_supervisors')

#             # Fetch the user based on the user_id
#             try:
#                 user = User.objects.get(id=user_id)
#                 print(f"User found: {user.username}")  # Debugging

#                 # Convert 'is_supervisor' to a boolean (adjusted conversion to handle different inputs)
#                 is_supervisor_value = request.POST.get('is_supervisor') == 'True'
#                 print(f"Supervisor status to update: {is_supervisor_value}")  # Debugging

#                 # Update and save the profile
#                 user.profile.is_supervisor = is_supervisor_value
#                 user.profile.save()
#                 print(f"Successfully updated {user.username}'s supervisor status to {user.profile.is_supervisor}")  # Debugging
#             except User.DoesNotExist:
#                 print("User does not exist")  # Debugging

#             return redirect('manage_supervisors')
#         else:
#             print("Form is not valid")  # Debugging

#     return render(request, 'manage_supervisors.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)

def manage_supervisors(request):
    # Ensure all users have a profile, linked to a User
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)
        # testing
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)  # Only create if profile does not exist

    # Retrieve users with profiles to display in the template
    users = User.objects.all()

    if request.method == 'POST':
        form = SupervisorForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user_id')
            if user_id:  # Ensure user_id exists in POST data
                try:
                    user = User.objects.get(id=user_id)
                    profile, created = Profile.objects.get_or_create(user=user)

                    # Update the supervisor status
                    is_supervisor_value = request.POST.get('is_supervisor') == 'True'
                    profile.is_supervisor = is_supervisor_value
                    profile.save()
                except User.DoesNotExist:
                    print("User does not exist")

            return redirect('manage_supervisors')

    return render(request, 'manage_supervisors.html', {'users': users})

def profile_setup(request):
    return render(request, 'profile_setup.html')


# def campaign_form(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         points = request.POST.get('points')
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         location = request.POST.get('location')
#         description = request.POST.get('description')
#         delivery_method = request.POST.get('delivery_method')
#         add_to_news = request.POST.get('add_to_news') == 'on'

#         # Save the campaign to the database
#         Campaign.objects.create(
#             name=name,
#             start_date=start_date,
#             end_date=end_date,
#             location=location,
#             description=description,
#             is_active=True  # Mark campaign as active upon creation
#         )

#         return redirect('supervisor')  # Redirect to the supervisor page
#     return render(request, 'campaign_form.html')

def campaign_form(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('campaign_form')
    else:
        form = CampaignForm()
    return render(request, 'campaign_form.html', {'form': form})

#@login_required
def delete_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    campaign.delete()
    return redirect('supervisor')
