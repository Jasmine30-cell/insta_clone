from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Post  # Your Post model

# -------------------------------
# LOGIN USER
# -------------------------------
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, "Account does not exist.")
            return redirect('SignUser')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.info(request, "Wrong Password.")
            return render(request, 'login.html')
        else:
            login(request, user)
            return redirect('FriendUser')  # Redirect to feed after login

    return render(request, 'login.html')

# -------------------------------
# SIGNUP USER
# -------------------------------
# -------------------------------
# SIGNUP USER
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def SignUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        profile_pic = request.FILES.get('profile_pic')

        if password1 != password2:
            messages.error(request, "Passwords don't match")
            return redirect('SignUser')

        try:
            user = User.objects.create_user(
                username=username,
                password=password1,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            
            # Save profile picture if provided
            if profile_pic:
                profile = user.profile
                profile.profile_pic = profile_pic
                profile.save()
            
            messages.success(request, "Account created successfully!")
            return redirect('loginUser')
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
    
    return render(request, 'signup.html')


# -------------------------------
# LOGOUT USER
# -------------------------------
def logoutUser(request):
    logout(request)
    return redirect('loginUser')

# -------------------------------
# FEED PAGE (STORIES + POSTS)
# -------------------------------

# def feedUser(request):  # Renamed from feed_view
#     posts = Post.objects.all().order_by('-created_at')
#     username = request.user.username
#     return render(request, 'feed.html', {'posts': posts, 'username': username})
from django.contrib.auth.models import User
from .models import Profile

@login_required
def feedUser(request):
    posts = Post.objects.all().order_by('-created_at')
    
    # Get suggested users (excluding current user and already followed)
    current_user_profile = request.user.profile
    suggested_users = User.objects.exclude(
        id=request.user.id
    ).exclude(
        id__in=current_user_profile.followers.all()
    ).order_by('?')[:5]  # Random 5 users
    
    return render(request, 'feed.html', {
        'posts': posts,
        'suggested_users': suggested_users,
        'username': request.user.username
    })
# -------------------------------
# OTHER VIEWS
# -------------------------------
@login_required
def FriendUser(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'friends.html', {'posts': posts})

@login_required
def ProfileUser(request):
    return render(request, 'profile.html', {'user': request.user})
# In your views.py
def profileUser(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')
    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'profile.html', context)

@login_required
def MessageUser(request):
    return render(request, 'message.html')

@login_required
def SearchUser(request):
    return render(request, 'search.html')

@login_required
def NotificationUser(request):
    return render(request, 'notification.html')

@login_required
def ExploreUser(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'explore.html', {'posts': posts})

@login_required
def ReelsUser(request):
    return render(request, 'reels.html')

@login_required
def CreateUser(request):
    return render(request, 'create.html')
from django.shortcuts import get_object_or_404, redirect
from .models import Post


# In your views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def search_page(request):
    # Get logged-in user details
    users = [
        {'id': request.user.id, 'username': request.user.username, 'profilePic': request.user.profile_pic.url}  # Assuming you have a profile_pic field
    ]
    
    # Add more users to this list (you can fetch this from your database)
    users += [
        {'id': 2, 'username': 'sara.khan', 'profilePic': 'https://i.pravatar.cc/150?img=12'},
        {'id': 3, 'username': 'john_doe', 'profilePic': 'https://i.pravatar.cc/150?img=3'}
    ]
    
    return render(request, 'search.html', {'users': users})
from django.http import JsonResponse

@login_required
def follow_user(request, username):
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, username=username)
        request.user.profile.followers.add(user_to_follow)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
@login_required
def feedUser(request):
    posts = Post.objects.all().order_by('-created_at')
    
    # Get current user's profile
    current_profile = request.user.profile
    
    # Get suggested users (excluding current user and already followed users)
    suggested_users = User.objects.exclude(
        id=request.user.id
    ).exclude(
        id__in=current_profile.followers.all()  # Users who follow the current profile
    ).order_by('?')[:5]  # Random 5 users
    
    return render(request, 'feed.html', {
        'posts': posts,
        'suggested_users': suggested_users,
        'username': request.user.username
    })

# views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def follow_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_to_follow = User.objects.get(username=data['user_id'])
            profile_to_follow = user_to_follow.profile
            
            if data['action'] == 'follow':
                request.user.profile.following.add(user_to_follow)
                profile_to_follow.followers.add(request.user)
            else:
                request.user.profile.following.remove(user_to_follow)
                profile_to_follow.followers.remove(request.user)
                
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    
    # In your views.py
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def upload_post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        
        if image:
            post = Post.objects.create(
                user=request.user,
                image=image,
                caption=caption
            )
            return redirect('profile')  # Redirect to profile page after upload
        
    return redirect('create_post')  # Redirect back if upload fails


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Post
from django.contrib.auth.decorators import login_required

@login_required
def create_post(request):
    if request.method == 'POST':
        try:
            image = request.FILES['image']  # Using direct access to force error if missing
            caption = request.POST.get('caption', '')
            
            # Create the post
            post = Post.objects.create(
                user=request.user,
                image=image,
                caption=caption
            )
            
            # Return success response
            return JsonResponse({
                'status': 'success',
                'message': 'Post created successfully',
                'redirect_url': '/profile/'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return render(request, 'create.html')

@login_required
def profile(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'profile.html', {'posts': posts})
    
    return render(request, 'create.html')