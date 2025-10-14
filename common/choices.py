"""
This module defines various Django model choices as enumerations using `models.TextChoices`.
These choices are used to standardize and restrict the values for specific fields across the application.
Classes:
    PostVisibility: Choices for post visibility settings (Public, Followers, Close Friends).
    ChatType: Choices for chat types (Direct, Group).
    MemberRole: Choices for member roles in a group or chat (Member, Admin).
    ListingStatus: Choices for the status of a listing (Active, Reserved, Sold).
    ListingCondition: Choices for the condition of a listing (Brand New, Used).
    EventVisibility: Choices for event visibility (Public, Link Only, Community).
    EventLevel: Choices for event difficulty level (Beginner, Intermediate, Advanced, All).
    ParticipantStatus: Choices for participant status in an event (Joined, Waitlisted, Left, Cancelled).
    UpdateType: Choices for types of updates (Text, Score).

"""

from django.db import models

class PostVisibility(models.TextChoices):
    PUBLIC = "public", "Public"
    FOLLOWERS = "followers", "Followers"
    CLOSE_FRIENDS = "close_friends", "Close friends"

class ChatType(models.TextChoices):
    DIRECT = "direct", "Direct"
    GROUP = "group", "Group"

class MemberRole(models.TextChoices):
    MEMBER = "member", "Member"
    ADMIN = "admin", "Admin"

class ListingStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    RESERVED = "reserved", "Reserved"
    SOLD = "sold", "Sold"

class ListingCondition(models.TextChoices):
    BRAND_NEW = "brand_new", "Brand new"
    USED = "used", "Used"

class EventVisibility(models.TextChoices):
    PUBLIC = "public", "Public"
    LINK_ONLY = "link_only", "Link only"
    COMMUNITY = "community", "Community"

class EventLevel(models.TextChoices):
    BEGINNER = "beginner", "Beginner"
    INTERMEDIATE = "intermediate", "Intermediate"
    ADVANCED = "advanced", "Advanced"
    ALL = "all", "All"

class ParticipantStatus(models.TextChoices):
    JOINED = "joined", "Joined"
    WAITLISTED = "waitlisted", "Waitlisted"
    LEFT = "left", "Left"
    CANCELLED = "cancelled", "Cancelled"

class UpdateType(models.TextChoices):
    TEXT = "text", "Text"
    SCORE = "score", "Score"
