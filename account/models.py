from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# class Post(models.Model):
#     MEDIA_TYPE_CHOICES = (
#         ('image', 'Image'),
#         ('video', 'Video'),
#     )
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     media = models.FileField(upload_to='media/')
#     media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
#     caption = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     likes = models.ManyToManyField(User, through='PostLike', related_name='liked_posts', blank=True)

#     def __str__(self):
#         return f"{self.user.username}'s post - {self.media_type}"
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s post"

class PostLike(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def follower_count(self):
        return self.followers.count()

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    from django.db import models
from django.contrib.auth.models import User

