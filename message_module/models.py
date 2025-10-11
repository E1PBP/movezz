from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from profile_module.models import Profile
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Conversations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_conversations')
    class ChatType(models.TextChoices):
        DIRECT = "direct", _("Direct")
        GROUP = "group", _("Group")

    chat_type = models.CharField(
        max_length=10,
        choices=ChatType.choices,
        default=ChatType.DIRECT,
    )
    
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    member_count = models.IntegerField(default=0)

    last_message_id = models.UUIDField(blank=True, null=True, editable=False)
    last_message_at = models.DateTimeField(blank=True, null=True, editable=False)
    last_message_preview = models.TextField(blank=True, null=True, editable=False)

    def update_last_message(self, message):
        self.last_message_id = message.id
        self.last_message_at = message.created_at
        self.last_message_preview = message.body[:100]
        self.save(update_fields=["last_message_id", "last_message_at", "last_message_preview"])
        
        
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Conversation {self.id} ({self.chat_type})"
    
    
    
class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    # conversation_id = models.UUIDField()
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    body = models.TextField()

    @property
    def sender_display_name(self):
        return getattr(self.sender.profile, 'display_name', self.sender.username)

    @property
    def sender_display_avatar(self):
        return getattr(self.sender.profile, 'avatar', "")
    conversation = models.ForeignKey('Conversations', on_delete=models.CASCADE, related_name='messages')
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender_display_name} at {self.created_at}"