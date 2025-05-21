import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserProfileForm
from .models import UserProfile

def create_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            image = form.cleaned_data['profile_photo_file']
            image_path = os.path.join('media/uploads', image.name)

            # Save file to disk
            full_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image.name)
            with open(full_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            instance.profile_photo = image_path  # save relative path to DB
            instance.save()
            return redirect('view_profiles')  # or any page
    else:
        form = UserProfileForm()
    return render(request, 'create_profile.html', {'form': form})


def edit_user_profile(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            instance = form.save(commit=False)
            if 'profile_photo_file' in request.FILES:
                image = form.cleaned_data['profile_photo_file']
                image_path = os.path.join('media/uploads', image.name)
                full_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image.name)
                with open(full_path, 'wb+') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                instance.profile_photo = image_path
            instance.save()
            return redirect('view_profiles')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

def view_profiles(request):
    profiles = UserProfile.objects.all()
    return render(request, 'view_profiles.html', {'profiles': profiles})

def delete_profile(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    profile.delete()
    return redirect('view_profiles')
