from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from taggit.models import Tag
# Create your models here.

class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
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


# class rating(models.Model):
#     user = models.ForeignKey(User)
#     commentID = models.ForeignKey(CommentPost,on_delete=models.CASCADE)
#     values = models.IntegerField()
#     def validate_unique(self, *args, **kwargs):
#         super(rating, self).validate_unique(*args, **kwargs)
#         if not self.id:
#             if self.__class__.objects.filter(user=self.user,commentID=self.commentID).exists():
#                 raise ValidationError(
#                     {
#                         NON_FIELD_ERRORS: [
#                             'Rating already exists',
#                         ],
#                     }
#                 )