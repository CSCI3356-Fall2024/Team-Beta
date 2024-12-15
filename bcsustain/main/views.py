#views.py is the business logic layer
#it contains the logic for handling requests and returning responses
 #Views retrieve data from models and pass it to templates for rendering

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
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import logout
from .forms import RewardForm
from .models import RedeemedReward, Reward
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)

@login_required #ensures that only authenticated users can access the view
def profile_setup(request): #users not logged in are redirected to login page
    profile, created = Profile.objects.get_or_create(user=request.user)
    #^^ tries to retrieve the Profile object associated with the logged in user, creating a new Profile otherwise
    profile_picture_url = (
        profile.profile_picture.url
        if profile.profile_picture and profile.profile_picture.url
        else '/static/profile_pictures/default_profile_pic.png'
    )

    if request.method == 'POST':
        if 'delete_photo' in request.POST:
            if profile.profile_picture:  # Check if a photo exists
                profile.profile_picture.delete(save=True)  # Delete the photo from the filesystem
                profile.profile_picture = None  # Clear the profile_picture field
                profile.save()
            messages.success(request, "Profile picture removed successfully.")
            return redirect('profile_setup')

        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            logger.info("FORM IS VALID")
            form.save()
            profile.refresh_from_db()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile_setup')
        else:
            messages.error(request, "There was an error updating your profile. Please try again.")
    else: #Handling 'GET' requests
        form = ProfileForm(instance=profile)
        #creates ProfileForm prefilled with user's current profile data
    context = {
        'form': form,
        'profile': profile,
        'profile_picture_url': profile_picture_url,
    }

    return render(request, 'profile_setup.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')


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

        if not email.endswith('@bc.edu'):
            messages.error(request, "Please use a valid @bc.edu email address.")
            return render(request, 'signup.html', {'form': form})

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html', {'form': form})

        if User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'signup.html', {'form': form})

        if form.is_valid():
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()

            # Create an associated Profile
            Profile.objects.create(user=user)

            auth_login(request, user)
            return redirect('landing')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

def custom_login(request):   #OMER ADDED THIS. JUST LEAVE IT FOR NOW. TRYING TO MAKE OUR LOGIN NOT GO TO THE DJANGO DEFAULT
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('landing')  # Redirect to the landing page after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})  # Display error message
    return render(request, 'login.html')  # Render the login template for GET requests

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
        form = RewardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Reward added successfully!")
            #return redirect('supervisorrewards')  # Redirect to the supervisor rewards page
            return redirect('rewards')
        else:
            messages.error(request, "There was an error adding the reward. Please check the form.")
    else:
        form = RewardForm()

    return render(request, 'add_reward.html', {'form': form})

# @user_passes_test(lambda u: u.is_superuser)  # Restrict access to superusers
def delete_rewards(request):
    rewards = Reward.objects.all()

    if request.method == 'POST':
        reward_id = request.POST.get('reward_id')
        reward = get_object_or_404(Reward, id=reward_id)
        reward.delete()
        messages.success(request, f"Reward '{reward.name}' has been deleted.")
        return redirect('delete_rewards')  # Refresh the manage rewards page

    return render(request, 'delete_rewards.html', {'rewards': rewards})


@login_required
def action(request):
    today = timezone.now().date()
    active_campaigns = Campaign.objects.filter(start_date__lte=today, end_date__gte=today, is_active=True)
    permanent_campaigns = Campaign.objects.filter(is_permanent=True)

    return render(request, 'action.html', {
        'active_campaigns': active_campaigns,
        'permanent_campaigns': permanent_campaigns,
    })

@login_required
def complete_campaign(request, id):
    # Retrieve the campaign by its ID
    campaign = get_object_or_404(Campaign, id=id)

    # Add points to the user's profile
    profile = request.user.profile
    profile.points += campaign.points
    profile.save()

    # Display a success message
    messages.success(request, f"You have gained {campaign.points} points!")

    # Check if the request came from the Action page or the Landing page
    referer = request.META.get('HTTP_REFERER', '')

    # Redirect logic based on the referring page
    if 'action' in referer:
        return redirect('action')  # Redirect to the Action Page
    else:
        return redirect('landing')

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
    # If the user is not authenticated, redirect them to the login page
    if not request.user.is_authenticated:
        return redirect('login')

    # Get the user's profile if it exists
    profile = getattr(request.user, 'profile', None)

    # Determine the user's role (Supervisor or Student) if logged in
    role = "Supervisor" if profile and getattr(profile, 'is_supervisor', False) else "Student"

    # Get active campaigns for today
    today = timezone.now().date()
    active_campaigns = Campaign.objects.filter(
        start_date__lte=today,
        end_date__gte=today,
        add_to_news=True
    )

    # Leaderboard
    leaderboard = Profile.objects.order_by('-points')[:5]

    return render(request, 'landing.html', {
        'active_campaigns': active_campaigns,
        'role': role,
        'leaderboard': leaderboard,
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
def add_permanent_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.is_permanent = True  # Ensure the campaign is marked as permanent
            form.save()
            messages.success(request, "Permanent campaign added successfully!")
            return redirect('action')
        else:
            messages.error(request, "There was an error adding the permanent campaign.")
    else:
        form = CampaignForm()

    return render(request, 'add_permanent_campaign.html', {'form': form})

#@login_required
def delete_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    campaign.delete()
    return redirect('supervisor')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reward, Profile



# @login_required
# def rewards(request):
#     rewards = Reward.objects.filter(available=True)  # Query available rewards
#     return render(request, 'rewards.html', {'rewards': rewards})

# Jacob Added this
@login_required
def redeem_reward(request, reward_id):
    reward = get_object_or_404(Reward, id=reward_id)
    user_profile = Profile.objects.get(user=request.user)

    # Check if the reward is available
    if not reward.is_available():
        messages.error(request, "This reward is not available or has expired.")
        return redirect('rewards')

    # Check if the user has enough points
    if user_profile.total_points() < reward.points_required:
        messages.error(request, "You do not have enough points to redeem this reward.")
        return redirect('rewards')

    # Deduct points by increasing points_spent
    user_profile.points_spent += reward.points_required
    user_profile.save()

    # Create a RedeemedReward entry
    RedeemedReward.objects.create(
        user=request.user,
        reward=reward,
        points_spent=reward.points_required,
    )

    # Success message
    messages.success(request, f"You successfully redeemed {reward.name}!")
    return redirect('rewards')

@login_required
def rewards(request):
    user_profile = Profile.objects.get(user=request.user)
    redeemed_rewards = RedeemedReward.objects.filter(user=request.user).order_by('-redeemed_at')
    rewards = Reward.objects.filter(available=True)  # or however you're querying rewards
    return render(request, 'rewards.html', {'rewards': rewards, 'redeemed_rewards': redeemed_rewards, 'profile': user_profile})


# def rewards_view(request):
#     user_profile = Profile.objects.get(user=request.user)  # Assuming a one-to-one relationship with User
#     return render(request, 'rewards.html', {'profile': user_profile})
