from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
import uuid
from django.urls import reverse
# Create your models here.

#uploading user files to a specific directory
def user_derectory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True, default=uuid.uuid1)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_derectory_path, verbose_name='Picture', null=True, blank=True)
    caption = models.CharField(max_length=100000, verbose_name='Caption', null=True, blank=True)
    posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        return reverse('post-details', args = [str(self.id)])
    
    def __str__(self):
        return self.caption if self.caption else 'Post without caption'
    
class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User,on_delete=models.CASCADE, related_name='following')
    
    
    
class Stream(models.Model):
    following = models.ForeignKey(User,on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='stram_user')
    post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True)
    date = models.DateField()
    
    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()
    def __str__(self):
        return f"{self.user} -->{self.following}"

    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')    
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='post_like')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    added = models.DateTimeField(auto_now_add=True)


post_save.connect(Stream.add_post, sender=Post)


    
    