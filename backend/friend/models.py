from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Friend(models.Model):
    class STATUS(models.TextChoices):
        PENDING = "P", "Pending"
        ACCEPTED = "A", "Accepted"
        REJECTED = "R", "Rejected"
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sentRequest')
    requested_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiveRequest')
    status = models.CharField(max_length=1, choices=STATUS.choices, default=STATUS.PENDING)

    def __str__(self):
        return f"{self.requested_by} ---- {self.status} ---- {self.requested_to}"