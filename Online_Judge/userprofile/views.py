from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
# Create your views here.
@login_required
def update_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('userprofile:update_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'userprofile/update_profile.html', {'form': form})
