from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings


def validate_participants(value):
    if value.count() > 2:
        raise ValidationError('The number of participants must be 2 or less.')


class Thread(models.Model):
    title = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.title

    def add_participant(self, user):
        if self.participants.count() >= 2:
            raise ValueError("Thread can't have more than 2 participants.")
        self.participants.add(user)


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    def mark_as_read(self):
        self.is_read = True
        self.save()