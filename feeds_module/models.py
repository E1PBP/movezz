import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from common.models import Sport, Hashtag
from cloudinary.models import CloudinaryField
from common.utils.validator_image import validate_image_size


class Post(models.Model):
    """
    Represents a user-generated post in the application.
    Attributes:
        id (UUIDField): A unique identifier for the post.
        user (ForeignKey): The user who created the post.
        text (TextField): The text content of the post.
        sport (ForeignKey): The sport associated with the post (can be null).
        location_name (CharField): The name of the location associated with the post (can be null).
        location_lat (DecimalField): The latitude of the location associated with the post (can be null).
        location_lng (DecimalField): The longitude of the location associated with the post (can be null).
        views_count (BigIntegerField): The number of views the post has received.
        likes_count (BigIntegerField): The number of likes the post has received.
        comments_count (BigIntegerField): The number of comments the post has received.
        author_display_name (CharField): The display name of the post's author.
        author_avatar_url (TextField): The URL of the post author's avatar.
        author_badges_url (TextField): The URL of the post author's badges.
        author_sports (TextField): The sports of the post author.
        created_at (DateTimeField): The date and time the post was created.
        updated_at (DateTimeField): The date and time the post was last updated.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True, blank=True)
    location_name = models.CharField(max_length=120, blank=True, null=True)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    views_count = models.BigIntegerField(default=0)
    likes_count = models.BigIntegerField(default=0)
    comments_count = models.BigIntegerField(default=0)
    author_display_name = models.CharField(max_length=80, blank=True, null=True) 
    author_avatar_url = models.TextField(blank=True, null=True)
    author_badges_url = models.TextField(blank=True, null=True)
    author_sports = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class PostImage(models.Model):
    """
    Represents an image associated with a post.
    Attributes:
        id (UUIDField): The unique identifier for the image.
        post (ForeignKey): A foreign key to the Post model, representing the post to which the image belongs.
                            Uses the related_name "images" for reverse relation.
                            Deletes the image when the associated post is deleted (CASCADE).
        image (CloudinaryField): A field for storing the image using Cloudinary.
                                 It accepts images, validates their size using validate_image_size,
                                 and allows null and blank values.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, related_name="images", on_delete=models.CASCADE)
    image = CloudinaryField("image", validators=[validate_image_size], null=True, blank=True)


class PostLike(models.Model):
    """
    Model representing a like on a post.
    Attributes:
        post (ForeignKey): The post that is liked.
        user (ForeignKey): The user who liked the post.
        created_at (DateTimeField): The timestamp when the like was created.
    Meta:
        unique_together (tuple): Ensures that a user can only like a post once.
    """
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("post", "user")

class Comment(models.Model):
    """
    Represents a comment on a post.
    Attributes:
        id (UUIDField): The unique identifier for the comment.
        post (ForeignKey): The post that the comment belongs to.
        user (ForeignKey): The user who created the comment.
        parent (ForeignKey): The parent comment, if any.
        text (TextField): The text of the comment.
        author_display_name (CharField): The display name of the comment's author.
        author_avatar_url (TextField): The URL of the comment author's avatar.
        created_at (DateTimeField): The date and time the comment was created.
        updated_at (DateTimeField): The date and time the comment was last updated.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    author_display_name = models.CharField(max_length=80, blank=True, null=True)
    author_avatar_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class CommentLike(models.Model):
    """
    Represents a user's like on a comment.
        Attributes:
            comment (ForeignKey): The comment that is liked.
            user (ForeignKey): The user who liked the comment.
            created_at (DateTimeField): The timestamp when the like was created.
        Meta:
            unique_together (tuple): Ensures that a user can only like a comment once.
    """
    
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("comment", "user")

class PostHashtag(models.Model):
    """
    Represents the relationship between a Post and a Hashtag.
    Attributes:
        post (ForeignKey): A foreign key to the Post model.
        hashtag (ForeignKey): A foreign key to the Hashtag model.
    Meta:
        unique_together (tuple): A tuple that defines the unique constraint for the model,
                                 ensuring that a post-hashtag combination is unique.
    """
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "hashtag")
