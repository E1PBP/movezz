from django.db import migrations

def add_is_active_if_missing(apps, schema_editor):
    vendor = schema_editor.connection.vendor
    if vendor == "postgresql":
        # Postgres: aman pakai IF NOT EXISTS
        schema_editor.execute("""
            ALTER TABLE marketplace_module_listing
            ADD COLUMN IF NOT EXISTS is_active boolean NOT NULL DEFAULT TRUE
        """)
    elif vendor == "sqlite":
        # SQLite 3.35+ sudah dukung IF NOT EXISTS (versimu 3.50.2)
        schema_editor.execute("""
            ALTER TABLE marketplace_module_listing
            ADD COLUMN IF NOT EXISTS is_active boolean DEFAULT 1
        """)
        # (SQLite bool=integer; NOT NULL + DEFAULT boleh, tapi DEFAULT saja sudah cukup)
    else:
        # Fallback: coba add column, jika sudah ada abaikan
        try:
            schema_editor.execute("""
                ALTER TABLE marketplace_module_listing
                ADD COLUMN is_active boolean
            """)
            schema_editor.execute("""
                UPDATE marketplace_module_listing SET is_active = TRUE WHERE is_active IS NULL
            """)
        except Exception:
            pass  # kolom sudah ada / engine tak mendukung, abaikan

class Migration(migrations.Migration):

    dependencies = [
        ("marketplace_module", "0006_fix_image_url_db_only"),
    ]

    operations = [
        # DB-only; state Django sudah menganggap field ini ada sejak 0001
        migrations.RunPython(add_is_active_if_missing, migrations.RunPython.noop),
    ]
