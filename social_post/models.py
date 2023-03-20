from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=10000)
    preview_pic = models.ImageField(upload_to="post/image", null=True, blank=True)
    caption = models.TextField()
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_by.username}'s post"

class Comment(models.Model) :
    body = models.TextField(max_length=1000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
        
    def __str__(self):
        return f"{self.created_by.username}'s comment"