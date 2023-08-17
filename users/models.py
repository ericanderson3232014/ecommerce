from django.db import models
from django.contrib.auth.models import User 




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    profile_image = models.ImageField(upload_to='profile_images')

    def __str__(self):
        return self.user.username
    
   
