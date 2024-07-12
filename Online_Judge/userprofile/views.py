from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('userprofile:update_profile')
    else:
        form = ProfileForm(instance=request.user.userprofile)
    
    return render(request, 'update_profile.html', {'form': form})


