from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.utils import timezone
from datetime import timedelta
import random
from common.models import Sport, Badge, Hashtag
from profile_module.models import Profile, UserSport, Follow, UserBadge
from faker import Faker

fake = Faker()


def create_or_get_sports(names=None):
    if names is None:
        names = [
            "Soccer", "Basketball", "Running", "Cycling",
            "Swimming", "Badminton", "Tennis", "Volleyball"
        ]
    created = []
    if Sport is None:
        return created
    for name in names:
        s, _ = Sport.objects.get_or_create(name=name, defaults={'icon': ''})
        created.append(s)
    return created


def create_or_get_badges(samples=None):
    if samples is None:
        samples = [
            ("rookie", "Rookie"),
            ("streak_7", "7-day Streak"),
            ("marathoner", "Marathoner"),
            ("social_butterfly", "Social Butterfly"),
            ("early_bird", "Early Bird"),
            ("night_owl", "Night Owl"),
        ]
    created = []
    if Badge is None:
        return created
    for code, name in samples:
        b, _ = Badge.objects.get_or_create(code=code, defaults={'name': name, 'icon_url': ''})
        created.append(b)
    return created


class Command(BaseCommand):
    help = "Seed profiles, sports, badges, follows, usersport and userbadge. No superuser will be created."

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=10, help="Jumlah pengguna dummy (default: 10)")
        parser.add_argument("--sports", type=int, default=6, help="Jumlah sport (default: 6)")
        parser.add_argument("--badges", type=int, default=6, help="Jumlah badge (default: 6)")
        parser.add_argument("--create-user", nargs=2, metavar=('USERNAME', 'PASSWORD'),
                            help="Buat akun spesifik: --create-user username password")
        parser.add_argument("--reset", action="store_true",
                            help="Hapus semua akun seed (prefix 'seeduser_') dan data terkait sebelum seed ulang")

    @transaction.atomic
    def handle(self, *args, **options):
        users_count = options["users"]
        sports_count = options["sports"]
        badges_count = options["badges"]
        create_user = options.get("create_user")
        do_reset = options.get("reset", False)

        self.stdout.write(self.style.MIGRATE_HEADING("Mulai seeding..."))

        if do_reset:
            self.stdout.write("Reset: menghapus semua user hasil seeding (email @example.com)...")
            qs = User.objects.filter(email__icontains="@example.com")
            count = qs.count()
            qs.delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted {count} seed users."))



        sport_names = [
            "Soccer", "Basketball", "Running", "Cycling",
            "Swimming", "Badminton", "Tennis", "Volleyball", "Climbing", "Boxing"
        ][:max(1, sports_count)]
        sports = create_or_get_sports(names=sport_names)

        badge_samples = [
            ("rookie", "Rookie"),
            ("streak_7", "7-day Streak"),
            ("marathoner", "Marathoner"),
            ("social_butterfly", "Social Butterfly"),
            ("early_bird", "Early Bird"),
            ("night_owl", "Night Owl"),
            ("goal_getter", "Goal Getter"),
            ("commander", "Community Leader"),
        ][:max(1, badges_count)]
        badges = create_or_get_badges(samples=badge_samples)


        if Hashtag is not None:
            tags = ["run", "fitness", "soccerlife", "cycling", "swim", "badminton"]
            for t in tags:
                Hashtag.objects.get_or_create(tag=t)

        created_users = []
        for i in range(users_count):
            username = fake.user_name()

            while User.objects.filter(username=username).exists():
                username = fake.user_name()

            email = f"{username}@example.com"
            password = "password12345"

            user = User.objects.create_user(username=username, password=password, email=email)

            profile_defaults = {
                "display_name": fake.name(),
                "bio": fake.sentence(nb_words=12) + " Saya suka olahraga dan komunitas.",
                "link": fake.url(),
                "current_sport": random.choice(sports) if sports else None,
                "post_count": random.randint(0, 50),
                "broadcast_count": random.randint(0, 20),
                "following_count": 0,
                "followers_count": 0,
                "is_verified": random.choice([False, False, True]),
                "created_at": timezone.now(),
                "updated_at": timezone.now()
            }
            Profile.objects.get_or_create(user=user, defaults=profile_defaults)

            created_users.append(user)

            if sports:
                chosen = random.sample(sports, k=min(len(sports), random.randint(1, 3)))
                for s in chosen:
                    hrs = random.randint(0, 200)
                    try:
                        UserSport.objects.get_or_create(user=user, sport=s, defaults={'time_elapsed': timedelta(hours=hrs)})
                    except Exception:
                        try:
                            UserSport.objects.get_or_create(user=user, sport=s, defaults={'time_elapsed': "0"})
                        except Exception:
                            pass

        for user in created_users:
            others = [u for u in created_users if u != user]
            n_follow = random.randint(0, min(4, len(others)))
            if n_follow == 0:
                continue
            to_follow = random.sample(others, k=n_follow)
            for followee in to_follow:
                try:
                    Follow.objects.get_or_create(follower=user, followee=followee)
                except IntegrityError:
                    pass

        for user in created_users:
            if not badges:
                break
            n_badges = random.randint(0, min(2, len(badges)))
            for b in random.sample(badges, k=n_badges):
                try:
                    UserBadge.objects.get_or_create(user=user, badge=b)
                except IntegrityError:
                    pass

        if create_user:
            uname, pwd = create_user
            if User.objects.filter(username=uname).exists():
                self.stdout.write(self.style.WARNING(f"User {uname} sudah ada, tidak membuat ulang."))
            else:
                u = User.objects.create_user(username=uname, password=pwd, email=f"{uname}@example.com")
                Profile.objects.create(user=u, display_name=uname, bio="Akun dibuat lewat seed script", link="")
                self.stdout.write(self.style.SUCCESS(f"Created user {uname}"))

        for user in created_users:
            try:
                profile = Profile.objects.get(user=user)
                profile.update_all_counts()
            except Profile.DoesNotExist:
                continue

        self.stdout.write(self.style.SUCCESS(f"Seeding selesai. Dibuat/diupdate {len(created_users)} users."))

