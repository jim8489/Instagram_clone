from django.db import models
from django.contrib.auth.models import User
from post.models import Post
from django.db.models.signals import post_save
from PIL import Image
# Create your models here.
#uploading user files to a specific directory
def user_derectory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank= True)
    url = models.URLField(max_length=1000, null=True, blank=True)
    bio = models.TextField(max_length=150, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=user_derectory_path, null=True, blank=True, default="default-user.png")
    
    def __str__(self):
        return f'{self.user.username} - Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300) 
            img.thumbnail(output_size)
            img.save(self.image.path)
    
