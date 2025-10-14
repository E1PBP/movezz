from django.db.models.signals import post_delete
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
import cloudinary.uploader


@receiver(post_delete)
def auto_delete_cloudinary_files(sender, instance, **kwargs):
    """
    Signal receiver to automatically delete Cloudinary files when a model instance with CloudinaryField is deleted.
    Args:
        sender (Model): The model class that sent the signal.
        instance (Model): The instance of the model that was deleted.
        **kwargs: Additional keyword arguments.
    Note:
        This function iterates through all fields of the model instance. If it finds any field that is an instance of CloudinaryField, it attempts to delete the associated file from Cloudinary using its public_id.
        If an error occurs during deletion, it catches the exception and prints a warning message.
    
    """
    for field in instance._meta.get_fields():
        if isinstance(field, CloudinaryField):
            image_field = getattr(instance, field.name, None)
            if image_field:
                try:
                    public_id = getattr(image_field, "public_id", None)
                    if public_id:
                        cloudinary.uploader.destroy(public_id)
                except Exception as e:
                    print(f"⚠️ Failed deleting file Cloudinary ({sender.__name__}.{field.name}): {e}")
