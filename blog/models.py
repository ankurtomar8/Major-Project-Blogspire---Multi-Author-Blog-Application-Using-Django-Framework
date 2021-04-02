from django.db import models
from  django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField



# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=150)
    content = RichTextField(blank=True , null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})    



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments" , on_delete=models.CASCADE) #delete all the comments to blog app if the post is deleted 
    name = models.CharField(max_length = 255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ' %s - %s ' % (self.post.title, self.name)