"""
    Testing the models of the social post application
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime

from django.db.utils import IntegrityError


from social_post.models import Post, Comment, Like
User = get_user_model()


class ModelTests(TestCase):
    """Testing models of social post application"""
    def setUp(self):
        """Create universal test variables for model test"""
        self.email = "test@123.com"
        self.username = "test"
        self.password = "thisIsTest@123"
        self.user = User.objects.create(email=self.email,username=self.username, password=self.password)
        # self.email1 = "test2@123.com"
        # self.username1 = "test2"
        # self.password1 = "thisIsTest@123222"
        # self.user = User.objects.create(email=self.email1,username=self.username1, password=self.password1)
        self.title = "This is a test title"
        self.content = "This is a test content"
        self.caption = "This is a caption"
        self.image = SimpleUploadedFile(name="test_image.jpg", content=b"", content_type="image/jpeg")
        

    def test_create_post(self):
        """Test creating new post"""
        post  = Post.objects.create(
            title=self.title,
            content=self.content,
            preview_pic=self.image,
            caption=self.caption,
            created_by=self.user
        )
        self.assertEqual(post.title, self.title)
        self.assertEqual(post.content, self.content)
        self.assertEqual(post.caption, self.caption)
        self.assertEqual(post.created_by, self.user)
        """check if auto created datetime is not null"""
        self.assertIsNotNone(post.created_at) 
        self.assertIsNotNone(post.updated_at)
        """check if auto created datetime is datetime object"""
        self.assertIsInstance(post.created_at, datetime)
        self.assertIsInstance(post.updated_at, datetime)
        """check if image filed object is not empty"""
        self.assertIsNotNone(post.preview_pic)
        """check if image extensions is correct"""
        self.assertTrue(post.preview_pic.name.endswith('.jpg'))
    
    def test_create_post_with_no_creator_raises_integrity_error(self):
        """Test creating new post with no creator raises integrity error"""
        with self.assertRaises(IntegrityError):
            Post.objects.create(
                title=self.title,
                content=self.content,
                preview_pic=self.image,
                caption=self.caption
            )
    
    def test_create_post_requires_auth_user(self):
        """Testing creating post requires auth auser"""
        self.client.login(username=self.username, password=self.password)
        post = Post.objects.create(
                title=self.title,
                content=self.content,
                preview_pic=self.image,
                caption=self.caption,
                created_by=self.user
            )
        self.assertEqual(post.created_by, self.user)
    
    def test_create_post_rejects_unauthenticated_user(self):
        with self.assertRaises(Exception):
            Post.objects.create(
                title=self.title,
                content=self.content,
                preview_pic=self.image,
                caption=self.caption
            )
    
    def test_create_comment(self):
        """Testing create comment by authenticated user"""
        self.client.login(username=self.username, password=self.password)
        post = Post.objects.create(
                title=self.title,
                content=self.content,
                preview_pic=self.image,
                caption=self.caption,
                created_by=self.user
            )
        comment = Comment.objects.create(
            body=self.content,
            post=post,
            created_by=self.user,
        )
        self.assertEqual(comment.body, self.content)
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.created_by, self.user)
        self.assertIsNotNone(comment.created_at)
        self.assertIsNotNone(comment.updated_at)
        self.assertIsInstance(comment.created_at, datetime)
        self.assertIsInstance(comment.updated_at, datetime)
        self.assertIsInstance(comment.created_by, User)
        self.assertIsInstance(comment.post, Post)
        self.assertTrue(comment.active)
    
    def test_create_comment_rejects_unauthenticated_user(self):
        """Test create comment rejects unauthenticated user"""
        post = Post.objects.create(
                title=self.title,
                content=self.content,
                preview_pic=self.image,
                caption=self.caption,
                created_by=self.user
            )
        with self.assertRaises(Exception):
            comment = Comment.objects.create(
                body=self.content,
                post=post
            )
    
    def test_create_comment_rejects_without_post(self):
        """Test create comment with out post raises error"""
        self.client.login(username=self.username, password=self.password)
        with self.assertRaises(Exception):
            comment = Comment.objects.create(
                body=self.content,
                created_by=self.user,
            )
    
    def test_create_like_auth_user(self):
        """Testing create like post by auth user"""
        self.client.login(username=self.username, password=self.password)
        post = Post.objects.create(
                title=self.title,
                content=self.content,
                preview_pic=self.image,
                caption=self.caption,
                created_by=self.user
            )
        like = Like.objects.create(post=post, created_by=self.user)
        self.assertEqual(like.post, post)
        self.assertIsInstance(like.post, Post)
        self.assertEqual(like.created_by, self.user)
        self.assertIsInstance(like.created_by, User)
    
    def test_create_like_rejects_unauth_user(self):
        """Testing like reject unauth user"""
        post = Post.objects.create(
                title=self.title,
                content=self.content,
                preview_pic=self.image,
                caption=self.caption,
                created_by=self.user
            )
        with self.assertRaises(Exception):
            Like.objects.create(post=post)
    
    def test_create_like_rejects_no_post(self):
        """Testing like reject no posts"""
        self.client.login(username=self.username, password=self.password)
        with self.assertRaises(Exception):
            Like.objects.create(created_by=self.user)