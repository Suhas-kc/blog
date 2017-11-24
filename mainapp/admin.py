from django.contrib import admin
from .models import CommentPost,BlogPost
# Register your models here.
admin.site.register(CommentPost)
admin.site.register(BlogPost)