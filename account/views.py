from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

# @login_required
# def friends_view(request):
#     # Your view logic here
#     return render(request, 'friends.html')
# def loginUser(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)

#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')

#             user = authenticate(username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('friends/')  # Redirect to friends page
#             else:
#                 messages.error(request, 'Invalid credentials')

#         else:
#             messages.error(request, 'Invalid form data')
    
#     else:
#         form = AuthenticationForm()

#     return render(request, 'login.html', {'form': form})

from django.contrib.auth.decorators import login_required
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request,"Account do not exists.")
            return redirect('SignUser')

        # Try to authenticate by username first
        user = authenticate(request, username=username, password=password)

        # If failed, try authenticating with email (if unique)
        if user is None:
            messages.info(request,"Wrong Password.")
            return render(request, 'login.html')
        else:
            login(request,user)
            return redirect('FriendUser')
           

        

    return render(request, 'login.html')

# @login_required
# def MessageUser(request):
#     user = request.user
#     return render(request, 'message.html', {'user': user})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def FriendUser(request):
    return render(request, 'friends.html')  # or whatever your template is



# def SignUser(request):
#     return render(request,'signup.html')
def SignUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('loginUser')

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
      
        messages.success(request, 'Account created successfully.Plz login')
        return redirect('loginUser')  # Redirect to friends page

    return render(request, 'signup.html')


# def logoutUser(request):
#     logout(user)
#     return render 

def ProfileUser(request):
    return render(request,'profile.html')
def MessageUser(request):
    return render(request,'message.html')
def SearchUser(request):
    return render(request,'search.html')
def NotificationUser(request):
    return render(request,'notification.html')
def ExploreUser(request):
    return render(request,'explore.html')
def ReelsUser(request):
    return render(request,'reels.html')
def CreateUser(request):
    return render(request,'create.html')
def ReelsUser(request):
   return render(request,'reels.html')
def ExploreUser(request):
    return render(request,'explore.html')




# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from django.contrib import messages

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username') or request.POST.get('username_or_email')  # adjust based on input name
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('/friends/')  # or use reverse('FriendUser') if you have a named URL
#         else:
#             messages.error(request, "Invalid credentials. Please try again.")
#             return render(request, 'login.html')

#     return render(request, 'login.html')
