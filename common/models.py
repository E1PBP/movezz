"""
This module defines common Django models that can be used across various modules in the project.
Models:
    - Sport: Represents a type of sport, with a unique name and optional icon.
    - Badge: Represents an achievement badge, identified by a unique code, name, and optional icon URL.
    - Hashtag: Represents a unique hashtag for categorization or tagging purposes.
Location:
    - This model is placed in the 'common' app to facilitate reuse in multiple modules.
"""

from django.db import models

class Sport(models.Model):
    """Model representing a sport.
    Attributes:
        id (BigAutoField): The primary key for the sport.
        name (CharField): The name of the sport (must be unique).
        icon (CharField): URL or path to the sport's icon (can be blank or null).
    Methods:
        __str__: Returns the name of the sport.
    """
    
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Badge(models.Model):
    """Model representing a badge that can be earned by users.
    Attributes:
        id (BigAutoField): The primary key for the badge.
        code (CharField): A unique code for the badge (max length 50).
        name (CharField): The name of the badge (max length 80).
        icon_url (CharField): URL to the badge's icon (max length 255), can be blank or null.
    """
    
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=80)
    icon_url = models.CharField(max_length=255, blank=True, null=True) # ini nanti insert manual aja di django admin pake link. ga usah pake cloudinary

    def __str__(self):
        return self.name

class Hashtag(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag
