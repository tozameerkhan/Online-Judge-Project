from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages
from .forms import PasswordUpdateForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
'''@login_required
def update_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('/home/homepage/')  # Redirect to the homepage after a successful update
    else:
        form = UserProfileForm(instance=user_profile)
        return render(request, 'profileview.html', {'form': form})
        return render(request, 'userprofile/profile.html', {'form': form})

    return redirect('/home/homepage/')
'''

@login_required
def view_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'view_profile.html', {'user_profile': user_profile})

@login_required
def update_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            #messages.info(request, 'Profile Updated Sucessfully!')
            return redirect('userprofile:view_profile')  # Redirect to view profile after update
    else:
        form = UserProfileForm(instance=user_profile)
        return render(request, 'update_profile.html', {'form': form})


    return redirect('userprofile:view_profile')
    

@login_required
def update_password(request):
    if request.method == 'POST':
        form = PasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session with the new password hash
            #messages.success(request, 'Your password was successfully updated!')
            #return redirect('userprofile:view_profile')  # Redirect to view profile after password change
            request.session['password_updated'] = True
            return redirect('/home/homepage/')
    else:
        form = PasswordUpdateForm(request.user)
    
    return render(request, 'update_password.html', {'form': form, 'username': request.user.username})