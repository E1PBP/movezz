from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from common.utils.validator_image import validate_image_size


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_conversations"
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    last_message_preview = models.CharField(max_length=200, blank=True, null=True)
    last_message_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_last_message(self, message):
        self.last_message_preview = message.body[:100] if message.body else "📷 Image"
        self.last_message_at = message.created_at
        self.save(update_fields=["last_message_preview", "last_message_at"])

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    body = models.TextField(blank=True)
    image = CloudinaryField("image", blank=True, null=True, validators=[validate_image_size])
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def sender_display_name(self):
        return getattr(self.sender.profile, "display_name", self.sender.username)

    @property
    def sender_display_avatar(self):
        return getattr(self.sender.profile, "avatar", "")

    def __str__(self):
        if self.image:
            return f"📷 Image from {self.sender_display_name}"
        return f"Message from {self.sender_display_name} at {self.created_at}"


class ConversationMember(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)
    last_read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("conversation", "user")

    def __str__(self):
        return f"{self.user} in {self.conversation}"
