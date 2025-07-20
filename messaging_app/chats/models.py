from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Extend the AbstractUser to create a custom user model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    
    def __str__(self):
        return self.username

# Conversation model to track participants in a conversation
class Conversation(models.Model):
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    participants = models.ManyToManyField(User, related_name='conversations')

    def __str__(self):
        return f"Conversation {self.conversation_id}"

# Message model to store messages in a conversation
class Message(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.username}"
