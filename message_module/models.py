from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from common.utils.validator_image import validate_image_size
from profile_module.models import Profile
from django.core.exceptions import ValidationError

class Conversation(models.Model):
    """A model representing a conversation between users.
    Attributes:
        id (UUIDField): The unique identifier for the conversation.
        created_by (ForeignKey): The user who created the conversation.
        title (CharField): An optional title for the conversation.
        last_message_preview (CharField): A preview of the last message in the conversation.
        last_message_at (DateTimeField): The timestamp of the last message in the conversation.
        created_at (DateTimeField): The timestamp when the conversation was created.
        updated_at (DateTimeField): The timestamp when the conversation was last updated.
    Methods:
        update_last_message(message): Updates the last message preview and timestamp.
        __str__(): Returns a string representation of the conversation.
    """
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

    def clean(self):
        """Ensure that a conversation has at most 2 members."""
        if self.pk and self.members.count() > 2:
            raise ValidationError("A private conversation can only have two members.")

    def get_participants(self):
        return User.objects.filter(conversationmember__conversation=self)
    

    def get_other_participant(self, user):
        return self.get_participants().exclude(id=user.id).first()
    
    def update_last_message(self, message):
        self.last_message_preview = message.body[:100] if message.body else "📷 Image"
        self.last_message_at = message.created_at
        self.save(update_fields=["last_message_preview", "last_message_at"])

    def __str__(self):
        members = ", ".join([u.username for u in self.get_participants()])
        return f"Conversation ({members})"


class Message(models.Model):
    """A model representing a message within a conversation.
    Attributes:
        id (UUIDField): The unique identifier for the message.
        conversation (ForeignKey): The conversation to which the message belongs.
        sender (ForeignKey): The user who sent the message.
        body (TextField): The text content of the message.
        image (CloudinaryField): An optional image associated with the message.
        created_at (DateTimeField): The timestamp when the message was created.
    Methods:
        sender_display_name(): Returns the display name of the sender.
        sender_display_avatar(): Returns the avatar URL of the sender.
        __str__(): Returns a string representation of the message.
    """
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
        if hasattr(self.sender, 'profile') and self.sender.profile:
            return getattr(self.sender.profile, "display_name", self.sender.username)

        sender_profile = Profile.objects.filter(user=self.sender).first()
        return getattr(sender_profile, "display_name", self.sender.username)

    @property
    def sender_display_avatar(self):
        if hasattr(self.sender, 'profile') and self.sender.profile:
            return getattr(self.sender.profile, "avatar_url", "") 
        sender_profile = Profile.objects.filter(user=self.sender).first()
        return getattr(sender_profile, "avatar_url", "")

    def __str__(self):
        if self.image:
            return f"📷 Image from {self.sender_display_name}"
        return f"Message from {self.sender_display_name} at {self.created_at}"


class ConversationMember(models.Model):
    """
    A model representing a member of a conversation.
    Attributes:
        conversation (ForeignKey): The conversation to which the member belongs.
        user (ForeignKey): The user who is a member of the conversation.
        joined_at (DateTimeField): The timestamp when the user joined the conversation.
        last_read_at (DateTimeField): The timestamp when the user last read messages in the conversation.
    Meta:
        unique_together (tuple): Ensures that a user can only be a member of a conversation once.
    Methods:
        __str__(): Returns a string representation of the conversation member.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="members"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)
    last_read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("conversation", "user")

    def clean(self):
        """Prevent adding more than 2 members to a conversation."""
        if self.conversation.members.exclude(pk=self.pk).count() >= 2:
            raise ValidationError("A private conversation can only have two members.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} in {self.conversation}"