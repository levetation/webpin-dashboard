from django.shortcuts import render, redirect
from .models import UserProfileModel
from boards.models import Board

# editable by user
def user_profile(request):
    context = {}
    

    try:
        profile = UserProfileModel.objects.get(account=request.user.id)
        context['profile'] = profile
    except UserProfileModel.DoesNotExist:
        # If the profile doesn't exist, you can create a new one
        profile = UserProfileModel.objects.create(account=request.user)
        context['profile'] = profile

    public_boards = Board.objects.filter(author=request.user, public=True)
    context['public_boards'] = public_boards

    if not public_boards.exists():
        context['no_public_boards'] = True
 
    if request.method == 'POST' and 'edit_profile' in request.POST:
        
        profile = UserProfileModel.objects.get(account=request.user.id)
        new_name = request.POST['name']
        if 'profile_picture' in request.FILES:
            profile.profile_picture.delete()
            profile_image = request.FILES['profile_picture']
        else: 
            profile_image = profile.profile_picture

        profile.name = new_name
        profile.profile_picture = profile_image
        profile.save()

        return redirect('user_profile')
    
    if request.method == 'POST' and 'remove_profile_picture' in request.POST:
        profile.profile_picture = None
        profile.save()

    return render(request, 'UserProfile/user_profile.html', context)
