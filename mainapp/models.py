from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.

class Post(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        abstract = True

class BlogPost(Post):
    title = models.CharField(max_length=100)
    tags = TaggableManager()

    class Meta:
        pass

class CommentPost(Post):
    postId = models.ForeignKey(BlogPost,on_delete=models.CASCADE)

    class Meta:
        pass