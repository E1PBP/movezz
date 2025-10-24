import json
from django.core.management.base import BaseCommand
from common.models import Sport

class Command(BaseCommand):
    help = 'Seeds the database with a list of popular sports.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding sports...'))

        sports_list = [
            "Soccer", "Basketball", "Tennis", "Baseball", "Golf", "Running",
            "Volleyball", "Badminton", "Swimming", "Boxing", "Table Tennis",
            "Skiing", "Ice Skating", "Roller Skating", "Cricket", "Rugby",
            "Pool", "Darts", "Football", "Bowling", "Ice Hockey", "Surfing",
            "Karate", "Horse Racing", "Snowboarding", "Skateboarding",
            "Cycling", "Archery", "Fishing", "Gymnastics", "Fencing",
            "Wrestling", "Judo", "Taekwondo", "Canoeing", "Bobsleigh",
            "Climbing", "Rowing", "Diving", "Equestrianism", "Handball",
            "Hockey", "Pentathlon", "Sailing", "Shooting", "Triathlon",
            "Weightlifting", "Softball", "Motocross", "Polo", "Cheerleading"
        ]

        for sport_name in sports_list:
            sport, created = Sport.objects.get_or_create(name=sport_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created Sport: {sport.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Sport "{sport.name}" already exists.'))

        self.stdout.write(self.style.SUCCESS('Sports seeding complete.'))
