from django.db import migrations

def add_image_url_if_missing(apps, schema_editor):
    vendor = schema_editor.connection.vendor
    if vendor == "postgresql":
        # Postgres: aman gunakan IF NOT EXISTS
        schema_editor.execute("""
            ALTER TABLE marketplace_module_listing
            ADD COLUMN IF NOT EXISTS image_url varchar(200)
        """)
    elif vendor == "sqlite":
        # SQLite 3.35+ mendukung IF NOT EXISTS; versimu 3.50.2 jadi aman
        schema_editor.execute("""
            ALTER TABLE marketplace_module_listing
            ADD COLUMN IF NOT EXISTS image_url varchar(200)
        """)
    else:
        # Fallback umum: coba tambah kolom; jika sudah ada, abaikan
        try:
            schema_editor.execute("""
                ALTER TABLE marketplace_module_listing
                ADD COLUMN image_url varchar(200)
            """)
        except Exception:
            pass  # kolom sudah ada / DB tidak mendukung, biarkan saja

class Migration(migrations.Migration):

    dependencies = [
        ("marketplace_module", "0005_merge_20251023_2331"),
    ]

    operations = [
        # DB-only; state Django sudah menganggap field ada dari 0001
        migrations.RunPython(add_image_url_if_missing, migrations.RunPython.noop),
    ]
