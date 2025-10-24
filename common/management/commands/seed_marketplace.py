# common/management/commands/seed_marketplace.py
import csv
import random
import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth.models import User
from django.conf import settings

import cloudinary
import cloudinary.uploader as cu

from marketplace_module.models import Listing, ListingImage

CITIES_ID = [
    "Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Semarang", "Depok",
    "Bekasi", "Tangerang", "Bogor", "Denpasar", "Makassar", "Medan",
    "Palembang", "Malang", "Solo", "Padang", "Pontianak"
]

def _config_cloudinary_from_settings():
    cfg = getattr(settings, "CLOUDINARY_STORAGE", {})
    cloudinary.config(
        cloud_name=cfg.get("CLOUD_NAME"),
        api_key=cfg.get("API_KEY"),
        api_secret=cfg.get("API_SECRET"),
        secure=True,
    )

def _first_sentence(text: str, limit: int = 120) -> str:
    if not text:
        return ""
    sentence = re.split(r"(?<=[.!?])\s+", text.strip())[0]
    return (sentence[:limit-1].rstrip() + "…") if len(sentence) > limit else sentence

def _rand_price():
    return int(round(random.randint(50_000, 2_000_000), -3))

def _pick_owner(owner_username: str | None):
    if owner_username:
        u = User.objects.filter(username=owner_username).first()
        if u:
            return u
        return User.objects.create_user(
            username=owner_username, password="password12345",
            email=f"{owner_username}@example.com"
        )
    ids = list(User.objects.values_list("id", flat=True))
    if not ids:
        return User.objects.create_user(
            username="seedmarket_seller",
            password="password12345",
            email="seedmarket_seller@example.com",
        )
    return User.objects.get(id=random.choice(ids))

# -------- Markdown sanitizer --------
_MD_CODEBLOCK = re.compile(r"```.*?```", flags=re.S)
_MD_IMAGE = re.compile(r"!\[([^\]]*)\]\([^)]+\)")
_MD_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_MD_BOLD = re.compile(r"(\*\*|__)(.*?)\1")
_MD_ITALIC = re.compile(r"(\*|_)(.*?)\1")
_MD_HEADERS = re.compile(r"(?m)^\s{0,3}#{1,6}\s*")
_MD_SETEXT = re.compile(r"(?m)^\s*[-=]{3,}\s*$")
_MD_BLOCKQUOTE = re.compile(r"(?m)^\s*>\s?")
_MD_UL = re.compile(r"(?m)^\s*[-*+]\s+")
_MD_OL = re.compile(r"(?m)^\s*\d+\.\s+")
_MD_HR = re.compile(r"(?m)^\s*([-*_]\s*){3,}\s*$")

def sanitize_markdown(md: str) -> str:
    """Remove common Markdown syntax, keep readable text."""
    if not md:
        return ""
    s = md.replace("\r\n", "\n")

    # remove code blocks & horizontal rules
    s = _MD_CODEBLOCK.sub("", s)
    s = _MD_HR.sub("", s)

    # images -> alt text; links -> text
    s = _MD_IMAGE.sub(r"\1", s)
    s = _MD_LINK.sub(r"\1", s)

    # bold/italic
    s = _MD_BOLD.sub(r"\2", s)
    s = _MD_ITALIC.sub(r"\2", s)

    # headers, setext underlines, blockquotes
    s = _MD_HEADERS.sub("", s)
    s = _MD_SETEXT.sub("", s)
    s = _MD_BLOCKQUOTE.sub("", s)

    # list markers
    s = _MD_UL.sub("", s)
    s = _MD_OL.sub("", s)

    # inline code/backticks
    s = s.replace("`", "")

    # remove any leftover asterisks/underscores
    s = s.replace("*", "").replace("_", "")

    # trim extra blank lines
    s = re.sub(r"\n{3,}", "\n\n", s)

    return s.strip()

class Command(BaseCommand):
    help = "Seed Listing marketplace dari CSV dan folder gambar + sanitasi markdown pada caption."

    def add_arguments(self, parser):
        parser.add_argument("--dataset-root", default="dataset-pbp")
        parser.add_argument("--csv", default="marketplace.csv")
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument("--owner-username", default=None)
        parser.add_argument("--upload-cloudinary", action="store_true",
                            help="Upload gambar via Cloudinary SDK dan simpan public_id ke CloudinaryField.")
        parser.add_argument("--image-base-url", default="",
                            help="Fallback untuk Listing.image_url jika tidak upload (mis. CDN statis).")
        parser.add_argument("--reset", action="store_true")

    def handle(self, *args, **opts):
        root = Path(opts["dataset_root"])
        csv_path = root / opts["csv"]
        img_dir = root / "marketplace"
        limit = opts["limit"] or None
        do_upload = bool(opts["upload_cloudinary"])
        base_url = opts["image_base_url"].rstrip("/")
        owner = _pick_owner(opts.get("owner_username"))

        if opts.get("reset"):
            self.stdout.write(self.style.WARNING("Menghapus semua Listing & ListingImage…"))
            ListingImage.objects.all().delete()
            Listing.objects.all().delete()

        if not csv_path.exists():
            raise CommandError(f"CSV tidak ditemukan: {csv_path}")
        if not img_dir.exists():
            self.stdout.write(self.style.WARNING(f"Folder gambar tidak ditemukan: {img_dir}"))

        if do_upload:
            _config_cloudinary_from_settings()

        rows = list(csv.DictReader(open(csv_path, "r", encoding="utf-8")))
        if limit:
            rows = rows[:limit]

        created = 0
        for row in rows:
            name = (row.get("name") or "").strip()
            raw_caption = (row.get("caption") or "").strip()
            if not name:
                continue

            # --- sanitize markdown ---
            caption = sanitize_markdown(raw_caption)

            try:
                with transaction.atomic():
                    listing = Listing.objects.create(
                        owner=owner,
                        title=_first_sentence(caption) or Path(name).stem.replace("_", " ").title(),
                        description=caption or "No description",
                        price=_rand_price(),
                        condition=random.choice([Listing.Condition.BRAND_NEW, Listing.Condition.USED]),
                        location=random.choice(CITIES_ID),
                        image_url="",
                        is_active=True,
                    )

                    local_img = img_dir / name
                    if do_upload and local_img.exists():
                        try:
                            result = cu.upload(
                                str(local_img),
                                folder="marketplace",
                                resource_type="image",
                                overwrite=True,
                            )
                            public_id = result.get("public_id")
                            secure_url = result.get("secure_url")
                            if public_id:
                                ListingImage.objects.create(listing=listing, image=public_id)
                            if secure_url:
                                listing.image_url = secure_url
                                listing.save(update_fields=["image_url"])
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f"Gagal upload gambar {name}: {e}"))
                    elif base_url:
                        listing.image_url = f"{base_url}/{name}"
                        listing.save(update_fields=["image_url"])

                    created += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Baris '{name}' dilewati karena error: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Berhasil membuat {created} listing marketplace (caption sudah dibersihkan)."))
