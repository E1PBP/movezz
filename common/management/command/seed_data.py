"""
Not done yet.
Intinya ini buat nge-seed database pake data palsu.
"""

from django.core.management.base import BaseCommand
from common.utils.seed_helpers import (
    fake_user, fake_post, fake_product, fake_message, fake_broadcast
)

class Command(BaseCommand):
    help = "Seed database with fake data"
