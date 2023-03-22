from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()



class Group(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Chat(models.Model):
    content = models.CharField(max_length=10000)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="messages")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_from_me")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_to_me")
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"From {self.from_user.username} to {self.to_user.username}: {self.content} [{self.created_at}]"