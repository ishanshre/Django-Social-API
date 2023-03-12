from django.contrib import admin

from social_post.models import Post, Comment
# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

@admin.register(Post)
class Post(admin.ModelAdmin):
    inlines = [CommentInline,]
    
