"""
URL configuration for instagramClone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account.views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',loginUser,name='loginUser'),
    path('sign/',SignUser,name='SignUser'),
    path('friends/',FriendUser,name='FriendUser'),
    
    path('profile/',ProfileUser,name='ProfileUser'),
    path('message/',MessageUser,name='MessageUser'),
    path("search/",SearchUser, name="SearchUser"),
    path("notification",NotificationUser,name='NotificationUser'),
    path("explore/",ExploreUser, name="ExploreUser"),
    path("reels/",ReelsUser, name="ReelsUser"),
    path("create/",CreateUser, name="CreateUser"),
    path("logout/",logoutUser,name='logoutUser'),
    # path("feed/",feedUser,name='feedUser'),
    path('follow/<str:username>/',follow_user, name='follow_user'),
    path('follow/<int:user_id>/',follow_user, name='follow_user'),
    path('follow-user/', follow_user, name='follow_user'),
    path('upload_post/', upload_post, name='upload_post'),
    path('create/', create_post, name='create_post'),
   
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
