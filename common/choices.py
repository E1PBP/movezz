"""
ini adalah file untuk menyimpan pilihan pilihan (enum type) yang digunakan di berbagai model
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
