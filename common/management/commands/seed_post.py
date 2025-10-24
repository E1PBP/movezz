import csv
import random
import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model

from django.conf import settings
import cloudinary
import cloudinary.uploader as cu

from common.models import Sport, Hashtag
from feeds_module.models import Post, PostImage, PostHashtag

User = get_user_model()
HASHTAG_REGEX = re.compile(r"#([A-Za-z0-9_]+)")

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

def _pick_user(author_username: str | None):
    if author_username:
        u = User.objects.filter(username=author_username).first()
        if u:
            return u
        return User.objects.create_user(
            username=author_username, password="password12345",
            email=f"{author_username}@example.com",
        )
    ids = list(User.objects.values_list("id", flat=True))
    if not ids:
        return User.objects.create_user(
            username="seedpost_author",
            password="password12345",
            email="seedpost_author@example.com",
        )
    return User.objects.get(id=random.choice(ids))

def _pick_sport_or_none():
    ids = list(Sport.objects.values_list("id", flat=True))
    if not ids:
        return None
    return Sport.objects.get(id=random.choice(ids)) if random.random() < 0.7 else None

def _extract_hashtags(text: str):
    if not text:
        return []
    seen, uniq = set(), []
    for t in HASHTAG_REGEX.findall(text):
        low = t.lower()
        if low not in seen:
            seen.add(low); uniq.append(low)
    return uniq

def _author_meta(user):
    display_name = user.username
    avatar_url = ""
    try:
        from profile_module.models import Profile
        prof = Profile.objects.filter(user=user).only("display_name", "avatar_url").first()
        if prof:
            display_name = prof.display_name or user.username
            avatar_url = getattr(prof, "avatar_url", "") or ""
    except Exception:
        pass
    return display_name, avatar_url

class Command(BaseCommand):
    help = "Seed Post dari CSV dan folder gambar."

    def add_arguments(self, parser):
        parser.add_argument("--dataset-root", default="dataset-pbp")
        parser.add_argument("--csv", default="post.csv")
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument("--author-username", default=None)
        parser.add_argument("--upload-cloudinary", action="store_true",
                            help="Upload gambar via Cloudinary SDK dan simpan public_id ke CloudinaryField.")
        parser.add_argument("--reset", action="store_true")
        parser.add_argument("--no-hashtags", action="store_true")

    def handle(self, *args, **opts):
        root = Path(opts["dataset_root"])
        csv_path = root / opts["csv"]
        img_dir = root / "post"
        limit = opts["limit"] or None
        do_upload = bool(opts["upload_cloudinary"])
        parse_hashtags = not bool(opts.get("no_hashtags"))

        if opts.get("reset"):
            self.stdout.write(self.style.WARNING("Menghapus semua PostImage, PostHashtag, dan Post…"))
            PostImage.objects.all().delete()
            PostHashtag.objects.all().delete()
            Post.objects.all().delete()

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
            caption = (row.get("caption") or "").strip()
            if not name:
                continue

            # savepoint per-row agar error 1 baris tidak merusak transaksi berikutnya
            try:
                with transaction.atomic():
                    user = _pick_user(opts.get("author_username"))
                    sport = _pick_sport_or_none()
                    author_display_name, author_avatar_url = _author_meta(user)

                    post = Post.objects.create(
                        user=user,
                        text=caption,
                        sport=sport,
                        location_name=random.choice(CITIES_ID) if random.random() < 0.3 else None,
                        location_lat=None,
                        location_lng=None,
                        views_count=random.randint(0, 5000),
                        likes_count=random.randint(0, 800),
                        comments_count=random.randint(0, 80),
                        author_display_name=author_display_name,
                        author_avatar_url=author_avatar_url,
                        author_badges_url="",
                        author_sports=(sport.name if sport else ""),
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                    )

                    # Upload gambar → simpan public_id ke CloudinaryField
                    local_img = img_dir / name
                    if do_upload and local_img.exists():
                        try:
                            result = cu.upload(
                                str(local_img),
                                folder="post",
                                resource_type="image",
                                overwrite=True,
                            )
                            public_id = result.get("public_id")
                            if public_id:
                                PostImage.objects.create(post=post, image=public_id)
                            else:
                                self.stdout.write(self.style.WARNING(f"Upload OK tapi tidak ada public_id untuk {name}"))
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f"Gagal upload gambar {name}: {e}"))

                    # Hashtags
                    if parse_hashtags and caption:
                        for t in _extract_hashtags(caption):
                            try:
                                ht, _ = Hashtag.objects.get_or_create(tag=t)
                                PostHashtag.objects.get_or_create(post=post, hashtag=ht)
                            except Exception as e:
                                self.stdout.write(self.style.WARNING(f"Gagal tautkan hashtag #{t}: {e}"))

                    created += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Baris '{name}' dilewati karena error: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Berhasil membuat {created} post."))
