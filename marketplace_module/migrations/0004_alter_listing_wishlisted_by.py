from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("marketplace_module", "0002_wishlist"),
        ("auth", "0012_alter_user_first_name_max_length"),  # versi auth default; sesuaikan jika berbeda
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                # Buang definisi M2M lama dari state
                migrations.RemoveField(
                    model_name="listing",
                    name="wishlisted_by",
                ),
                # Tambah lagi M2M dengan through=Wishlist
                migrations.AddField(
                    model_name="listing",
                    name="wishlisted_by",
                    field=models.ManyToManyField(
                        to=settings.AUTH_USER_MODEL,
                        related_name="wishlisted_listings",
                        blank=True,
                        through="marketplace_module.Wishlist",
                        through_fields=("listing", "user"),
                    ),
                ),
            ],
        ),
    ]
